// -*- tab-width: 8; indent-tabs-mode: nil; c-basic-offset: 4 -*-
// vi: set et ts=8 sw=4 sts=4:

//File that uses the tnnmg module instead of dune-fufem

#include <config.h>

#include <array>
#include <iostream>
#include <sstream>

// dune-common includes
#include <dune/common/bitsetvector.hh>
#include <dune/common/parallel/mpihelper.hh>
#include <dune/common/stringutility.hh>
#include <dune/common/test/testsuite.hh>

// dune-istl includes
#include <dune/istl/bcrsmatrix.hh>

// dune-grid includes
#include <dune/grid/yaspgrid.hh>
#include <dune/grid/io/file/vtk/vtkwriter.hh>

// dune-solver includes
#include <dune/solvers/common/defaultbitvector.hh>
#include <dune/solvers/iterationsteps/obstacletnnmgstep.hh>
#include <dune/solvers/iterationsteps/multigridstep.hh>
#include <dune/solvers/iterationsteps/truncatedblockgsstep.hh>
#include <dune/solvers/norms/energynorm.hh>
#include <dune/solvers/solvers/loopsolver.hh>
#include <dune/solvers/transferoperators/compressedmultigridtransfer.hh>


//dune-fufem includes
#include <dune/fufem/assemblers/transferoperatorassembler.hh>
#include <dune/fufem/utilities/gridconstruction.hh>

// dune-tnnmg includes
#include <dune/tnnmg/functionals/quadraticfunctional.hh>
#include <dune/tnnmg/functionals/boxconstrainedquadraticfunctional.hh>
#include <dune/tnnmg/functionals/bcqfconstrainedlinearization.hh>
#include <dune/tnnmg/iterationsteps/nonlineargsstep.hh>
#include <dune/tnnmg/iterationsteps/tnnmgstep.hh>

#include <dune/tnnmg/localsolvers/scalarobstaclesolver.hh>

#include <dune/tnnmg/projections/obstacledefectprojection.hh>

#include <dune/common/fvector.hh>
#include <dune/common/fmatrix.hh>

#include <dune/istl/matrixindexset.hh>

#include <dune/geometry/quadraturerules.hh>

#include <dune/localfunctions/lagrange/pqkfactory.hh>

#include <dune/matrix-vector/addtodiagonal.hh>

#include <dune/solvers/common/defaultbitvector.hh>
#include <dune/solvers/norms/energynorm.hh>
#include <dune/solvers/norms/twonorm.hh>


template<class GridView, class Matrix>
void constructPQ1Pattern(const GridView& gridView, Matrix& matrix)
{
    static const int dim = GridView::Grid::dimension;

    typedef typename Dune::PQkLocalFiniteElementCache<double, double, dim, 1> FiniteElementCache;
    typedef typename FiniteElementCache::FiniteElementType FiniteElement;

    const auto& indexSet = gridView.indexSet();
    FiniteElementCache cache;

    int size = indexSet.size(dim);

    Dune::MatrixIndexSet indices(size, size);

    for (const auto& element : elements(gridView))
    {
        const FiniteElement& fe = cache.get(element.type());

        int localSize = fe.size();
        for (int i = 0; i < localSize; ++i)
        {
            int iGlobal = indexSet.subIndex(element, fe.localCoefficients().localKey(i).subEntity(), dim);
            for (int j = 0; j < localSize; ++j)
            {
                int jGlobal = indexSet.subIndex(element, fe.localCoefficients().localKey(j).subEntity(), dim);
                indices.add(iGlobal, jGlobal);
                indices.add(jGlobal, iGlobal);
            }
        }
    }
    indices.exportIdx(matrix);
}

template<class GridView, class Matrix>
void assemblePQ1Stiffness(const GridView& gridView, Matrix& matrix)
{
    static constexpr int dim = GridView::Grid::dimension;
    static constexpr int dimworld = GridView::Grid::dimensionworld;

    typedef typename Dune::PQkLocalFiniteElementCache<double, double, dim, 1> FiniteElementCache;
    typedef typename FiniteElementCache::FiniteElementType FiniteElement;

    typedef typename Dune::FieldVector<double, dimworld> GlobalCoordinate;
    typedef typename FiniteElement::Traits::LocalBasisType::Traits::JacobianType JacobianType;

    const auto& indexSet = gridView.indexSet();
    FiniteElementCache cache;

    for (const auto& element : elements(gridView))
    {
        const auto& geometry = element.geometry();
        const FiniteElement& fe = cache.get(element.type());

        int localSize = fe.size();

        // get quadrature rule of appropiate order (P1/Q1)
        int order = (element.type().isSimplex())
                    ? 2*(1-1)
                    : 2*(dim-1);
        const auto& quad = Dune::QuadratureRules<double, dim>::rule(element.type(), order);

        // store gradients of shape functions and base functions
        std::vector<JacobianType> referenceGradients(localSize);
        std::vector<GlobalCoordinate> gradients(localSize);

        for (const auto& pt : quad)
        {
            // get quadrature point
            const auto& quadPos = pt.position();

            // get transposed inverse of Jacobian of transformation
            const auto invJacobian = geometry.jacobianInverseTransposed(quadPos);

            // get integration factor
            const double integrationElement = geometry.integrationElement(quadPos);

            // evaluate gradients of shape functions
            fe.localBasis().evaluateJacobian(quadPos, referenceGradients);

            // transform gradients
            for (size_t i=0; i<gradients.size(); ++i)
                invJacobian.mv(referenceGradients[i][0], gradients[i]);

            // compute matrix entries
            double z = pt.weight() * integrationElement;
            for (int i = 0; i < localSize; ++i)
            {
                int iGlobal = indexSet.subIndex(element, fe.localCoefficients().localKey(i).subEntity(), dim);
                for (int j = i+1; j < localSize; ++j)
                {
                    int jGlobal = indexSet.subIndex(element, fe.localCoefficients().localKey(j).subEntity(), dim);

                    double zij = (gradients[i] * gradients[j]) * z;
                    Dune::MatrixVector::addToDiagonal(matrix[iGlobal][jGlobal], zij);
                    Dune::MatrixVector::addToDiagonal(matrix[jGlobal][iGlobal], zij);
                }
                double zii = (gradients[i] * gradients[i]) * z;
                Dune::MatrixVector::addToDiagonal(matrix[iGlobal][iGlobal], zii);
            }
        }
    }
}


template<class GridView, class Matrix>
void assemblePQ1Mass(const GridView& gridView, Matrix& matrix)
{
    static const int dim = GridView::Grid::dimension;

    typedef typename Dune::PQkLocalFiniteElementCache<double, double, dim, 1> FiniteElementCache;
    typedef typename FiniteElementCache::FiniteElementType FiniteElement;

    typedef typename FiniteElement::Traits::LocalBasisType::Traits::RangeType RangeType;

    const auto& indexSet = gridView.indexSet();
    FiniteElementCache cache;

    for (const auto& element : elements(gridView))
    {
        const auto& geometry = element.geometry();
        const FiniteElement& fe = cache.get(element.type());

        int localSize = fe.size();

        // get quadrature rule of appropriate order (P1/Q1)
        int order = (element.type().isSimplex())
                    ? 2*1
                    : 2*dim;
        const auto& quad = Dune::QuadratureRules<double, dim>::rule(element.type(), order);

        // store values of shape functions
        std::vector<RangeType> values(localSize);

        for (size_t pt=0; pt < quad.size(); ++pt)
        {
            // get quadrature point
            const auto& quadPos = quad[pt].position();

            // get integration factor
            const double integrationElement = geometry.integrationElement(quadPos);

            // evaluate basis functions
            fe.localBasis().evaluateFunction(quadPos, values);

            // compute matrix entries
            double z = quad[pt].weight() * integrationElement;
            for (int i = 0; i < localSize; ++i)
            {
                int iGlobal = indexSet.subIndex(element, fe.localCoefficients().localKey(i).subEntity(), dim);
                double zi = values[i]*z;
                for (int j = i+1; j < localSize; ++j)
                {
                    int jGlobal = indexSet.subIndex(element, fe.localCoefficients().localKey(j).subEntity(), dim);

                    double zij = values[j] * zi;
                    Dune::MatrixVector::addToDiagonal(matrix[iGlobal][jGlobal], zij);
                    Dune::MatrixVector::addToDiagonal(matrix[jGlobal][iGlobal], zij);
                }
                double zii = values[i] * zi;
                Dune::MatrixVector::addToDiagonal(matrix[iGlobal][iGlobal], zii);
            }
        }
    }
}


template<class GridView, class Vector, class Function>
void assemblePQ1RHS(const GridView& gridView, Vector& r, const Function& f)
{
    static const int dim = GridView::Grid::dimension;

    typedef typename Dune::PQkLocalFiniteElementCache<double, double, dim, 1> FiniteElementCache;
    typedef typename FiniteElementCache::FiniteElementType FiniteElement;

    typedef typename FiniteElement::Traits::LocalBasisType::Traits::RangeType RangeType;

    const auto& indexSet = gridView.indexSet();
    FiniteElementCache cache;

    for (const auto& element : elements(gridView))
    {
        const auto& geometry = element.geometry();
        const FiniteElement& fe = cache.get(element.type());

        int localSize = fe.size();

        // get quadrature rule of appropiate order (P1/Q1)
        int order = (element.type().isSimplex())
                    ? 2*1
                    : 2*dim;

        const auto& quad = Dune::QuadratureRules<double, dim>::rule(element.type(), order);

        // store values of shape functions
        std::vector<RangeType> values(localSize);

        for (const auto& pt : quad)
        {
            // get quadrature point
            const auto& quadPos = pt.position();

            // get integration factor
            const double integrationElement = geometry.integrationElement(quadPos);

            // evaluate basis functions
            fe.localBasis().evaluateFunction(quadPos, values);

            // evaluate function
            auto fAtPos = f(geometry.global(quadPos));

            // add vector entries
            double z = pt.weight() * integrationElement;
            for (int i = 0; i < localSize; ++i)
            {
                int iGlobal = indexSet.subIndex(element, fe.localCoefficients().localKey(i).subEntity(), dim);

                r[iGlobal].axpy(values[i]*z, fAtPos);
            }
        }
    }
}


template<class Intersection>
bool intersectionContainsVertex(const Intersection& i, int vertexInInsideElement)
{
    static const int dim = Intersection::Entity::dimension;

    int faceIdx = i.indexInInside();

    const auto& refElement = Dune::ReferenceElements<double, dim>::general(i.inside().type());

    for (int j = 0; j<refElement.size(faceIdx, 1, dim); ++j)
    {
        int intersectionVertexInElement = refElement.subEntity(faceIdx, 1, j, dim);

        if (intersectionVertexInElement == vertexInInsideElement)
            return true;
    }
    return false;
}


template<class GridView, class BitVector>
void markBoundaryDOFs(const GridView& gridView, BitVector& isBoundary)
{
    static const int dim = GridView::Grid::dimension;

    typedef typename GridView::IndexSet IndexSet;
    typedef typename Dune::PQkLocalFiniteElementCache<double, double, dim, 1> FiniteElementCache;
    typedef typename FiniteElementCache::FiniteElementType FiniteElement;

    const IndexSet& indexSet = gridView.indexSet();
    FiniteElementCache cache;

    for (const auto& e : elements(gridView))
    {
        const FiniteElement& fe = cache.get(e.type());
        int localSize = fe.localBasis().size();

        for (const auto& i : intersections(gridView, e))
        {
            if (i.boundary())
            {
                for (int j = 0; j < localSize; ++j)
                {
                    unsigned int vertexInInsideElement = fe.localCoefficients().localKey(j).subEntity();
                    int iGlobal = indexSet.subIndex(e, vertexInInsideElement, dim);
                    if (intersectionContainsVertex(i, vertexInInsideElement))
                        isBoundary[iGlobal] = true;
                }
            }
        }
    }
}





//stripped down version of solving obstacle problem by truncated non-smooth newton multi-grid method
template<class GridViewType, class MatrixType, class VectorType>
void solveObstacleProblemByTNNMG(const GridViewType& gridview,
        const MatrixType& mat, VectorType& x, const VectorType& rhs,
        const VectorType& lower, const VectorType& upper,
        int dimPhaseField,
        int maxIterations=100, double tolerance=1.0e-10)
{
    const int blockSize = VectorType::block_type::dimension;

    //todo
    //do all the marking of the boudary DOF inside here at the moment, eventually export into python
    typedef typename ObstacleTNNMGStep<MatrixType, VectorType>::BitVector BitVector;
    BitVector ignore(rhs.size());
    ignore.unsetAll();
    if (blockSize > dimPhaseField)
        for (unsigned int n=0;n<rhs.size();++n)
           for (unsigned int i=dimPhaseField;i<blockSize;++i)
                ignore[n][i] = true;

    typedef VectorType Vector;
    typedef MatrixType Matrix;
    typedef EnergyNorm<Matrix, Vector> Norm;
    typedef ::LoopSolver<Vector> Solver;
    typedef ObstacleTNNMGStep<Matrix, Vector> TNNMGStep;
    typedef typename TNNMGStep::Transfer Transfer;
    typedef typename TNNMGStep::BoxConstraintVector BoxConstraintVector;
    typedef CompressedMultigridTransfer<Vector, BitVector, Matrix> TransferImplementation;

    //assemble hierarchy of matricies all at once
    using TOA = TransferOperatorAssembler<GridViewType>;
    // std::vector<std::shared_ptr<Matrix>> transfer_mat;
    std::vector<std::shared_ptr<Dune::BCRSMatrix<Dune::FieldMatrix<double, 1,1>>>> transfer_mat;
    TOA toa(gridview);
    toa.assembleMatrixHierarchy(transfer_mat);

    //needs to be gridview.hierarchicalGrid.maxLevel()
    std::vector<std::shared_ptr<Transfer>> transfer(gridview.grid().maxLevel());

    //now put this matrix hierarchy into a hierarchy of Transfer objects
    for (size_t i = 0; i < transfer.size(); i ++)
    {
        auto t = std::make_shared<TransferImplementation>(transfer_mat[i]);
        transfer[i] = t;
    }

    using Functional = Dune::TNNMG::BoxConstrainedQuadraticFunctional<Matrix&, Vector&, Vector&, Vector&, double>;
    auto J = Functional(mat, rhs, lower, upper);

    auto localSolver = gaussSeidelLocalSolver(Dune::TNNMG::ScalarObstacleSolver());

    using NonlinearSmoother = Dune::TNNMG::NonlinearGSStep<Functional, decltype(localSolver), BitVector>;
    auto nonlinearSmoother = std::make_shared<NonlinearSmoother>(J, x, localSolver);

    auto smoother = TruncatedBlockGSStep<Matrix, Vector>{};

    auto linearMultigridStep = std::make_shared<Dune::Solvers::MultigridStep<Matrix, Vector> >();
    linearMultigridStep->setMGType(1, 3, 3);
    linearMultigridStep->setSmoother(&smoother);
    linearMultigridStep->setTransferOperators(transfer);

    using Linearization = Dune::TNNMG::BoxConstrainedQuadraticFunctionalConstrainedLinearization<Functional, BitVector>;
    using DefectProjection = Dune::TNNMG::ObstacleDefectProjection;
    using LineSearchSolver = Dune::TNNMG::ScalarObstacleSolver;
    using Step = Dune::TNNMG::TNNMGStep<Functional, BitVector, Linearization, DefectProjection, LineSearchSolver>;

    using Solver = LoopSolver<Vector>;
    using Norm =  EnergyNorm<Matrix, Vector>;


    using Step = Dune::TNNMG::TNNMGStep<Functional, BitVector, Linearization, DefectProjection, LineSearchSolver>;
    int mu=1; // #multigrid steps in Newton step
    auto step = Step(J, x, nonlinearSmoother, linearMultigridStep, mu, DefectProjection(), LineSearchSolver());

    auto norm = Norm(mat);
    auto solver = Solver(step, 1e9, 0, norm, Solver::FULL);

    step.setIgnore(ignore);
    step.setPreSmoothingSteps(3);

    solver.addCriterion(
            [&](){
            return Dune::formatString("   % 12.5e", J(x));
            },
            "   energy      ");

    double initialEnergy = J(x);
    solver.addCriterion(
            [&](){
            static double oldEnergy=initialEnergy;
            double currentEnergy = J(x);
            double decrease = currentEnergy - oldEnergy;
            oldEnergy = currentEnergy;
            return Dune::formatString("   % 12.5e", decrease);
            },
            "   decrease    ");

    solver.addCriterion(
            [&](){
            return Dune::formatString("   % 12.5e", step.lastDampingFactor());
            },
            "   damping     ");


    solver.addCriterion(
            [&](){
            return Dune::formatString("   % 12d", step.linearization().truncated().count());
            },
            "   truncated   ");


    std::vector<double> correctionNorms;
    solver.addCriterion(Dune::Solvers::correctionNormCriterion(step, norm, 1e-10, correctionNorms));

    solver.preprocess();
    solver.solve();
    std::cout << correctionNorms.size() << std::endl;
}
