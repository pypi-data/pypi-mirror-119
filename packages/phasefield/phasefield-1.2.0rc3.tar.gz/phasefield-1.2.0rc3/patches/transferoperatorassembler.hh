// -*- tab-width: 8; indent-tabs-mode: nil; c-basic-offset: 4 -*-
// vi: set ts=8 sw=4 et sts=4:
#ifndef DUNE_FUFEM_ASSEMBLERS_TRANSFER_OPERATOR_ASSEMBLER_HH
#define DUNE_FUFEM_ASSEMBLERS_TRANSFER_OPERATOR_ASSEMBLER_HH

#include <vector>
#include <map>
#include <memory>

#include <dune/istl/matrixindexset.hh>
#include <dune/common/bitsetvector.hh>
#include <dune/common/timer.hh>
#include <dune/geometry/referenceelements.hh>

#include <dune/fufem/functionspacebases/dunefunctionsbasis.hh>
#include <dune/functions/functionspacebases/lagrangebasis.hh>

template <class GridView>
class MultilevelBasis
{
    private:
        typedef typename GridView::Grid GridType;
        static const int dim = GridType::dimension;

    public:
        typedef typename GridType::template Codim<0>::Entity Element;
        typedef DuneFunctionsBasis<Dune::Functions::LagrangeBasis<typename GridType::LevelGridView, 1> > LevelBasis;
        typedef typename LevelBasis::LocalFiniteElement LocalFiniteElement;

        MultilevelBasis(const GridView& gridview) :
            gridView(gridview), grid(gridview.grid()),
            idSet(gridView.grid().localIdSet())
        {
            const auto& leafIndexSet = gridView.indexSet();

            int maxLevel = grid.maxLevel();

            levelBasis_.resize(maxLevel+1);
            for(int level=0; level<=maxLevel; ++level)
                levelBasis_[level] = std::make_shared<LevelBasis>(grid.levelGridView(level));

            idToIndex.resize(maxLevel+1);
            size_.resize(maxLevel+1);

            size_[maxLevel] = grid.size(dim);

            // build extended level indices as map (id -> index)
            // 1. enumerate vertices on each level
            // 2. enumerate leaf vertices on each finer level to emulate copies of them
            // 3. on maxlevel take the leaf indices
            //
            // example: level=*, copy=(*), leaf=[*]
            // 
            //  [1] -  -  -  -  -  -  - [2]---[3]---[4] -  -  - [5]
            //   
            //  (4) -  -  -  -  -  -  -  1-----------2-----------3
            // 
            //   1-----------------------2-----------------------3

            // first use the level indices
            for(int level=0; level<maxLevel; ++level)
            {
                const auto& indexSet = grid.levelIndexSet(level);
                size_[level] = indexSet.size(dim);
                for (const auto& it : vertices(grid.levelGridView(level)))
                    idToIndex[level][idSet.id(it)] = indexSet.index(it);
            }

            for (const auto& it : vertices(gridView))
            {
                idToIndex[maxLevel][idSet.id(it)] = leafIndexSet.index(it);

                for(int level=it.level()+1; level<maxLevel; ++level)
                {
                    idToIndex[level][idSet.id(it)] = size_[level];
                    ++size_[level];
                }
            }
        }

        const LocalFiniteElement& getLocalFiniteElement(const Element& e) const
        {
            return levelBasis_[e.level()]->getLocalFiniteElement(e);
        }

        int size(int level)
        {
            return size_[level];
        }

        int index(const Element& e, const int i, const int level) const
        {
            const Dune::LocalKey& localKey = getLocalFiniteElement(e).localCoefficients().localKey(i);
            const IdType id = idSet.subId(e, localKey.subEntity(), localKey.codim());
            return idToIndex[level].find(id)->second;
        }


    private:
        const GridView& gridView;
        const GridType& grid;
        const typename GridType::LocalIdSet& idSet;
        std::vector<std::shared_ptr<LevelBasis> > levelBasis_;

        typedef typename GridType::Traits::LocalIdSet::IdType IdType;
        std::vector< std::map<IdType,int> > idToIndex;
        std::vector<int> size_;
};


//! Assembler for a hierarchy of multigrid transfer operators
template <class GridType>
class TransferOperatorAssembler {

    public:
        template <typename U = GridType, typename = decltype(std::declval<U>().grid().maxLevel() )>
        TransferOperatorAssembler(const GridType& gridView) :
            grid(gridView), maxLevel(gridView.grid().maxLevel())
        {}
        template <typename U = GridType, typename = decltype(std::declval<U>().grid().maxLevel() )>
        const auto levelGridView(int level) const
        {
            return grid.grid().levelGridView(level);
        }

        template <typename U = GridType, typename = decltype(std::declval<U>().maxLevel() ), int = 1 >
        TransferOperatorAssembler(const GridType& grid) :
            grid(grid), maxLevel(grid.maxLevel())
        {}
        template <typename U = GridType, typename = decltype(std::declval<U>().maxLevel() ), int = 1 >
        const auto levelGridView(int level) const
        {
            return grid.levelGridView(level);
        }

        template <class TransferOperator>
        void assembleOperatorHierarchy(std::vector<TransferOperator>& T) const
        {
            std::vector <typename TransferOperator::TransferOperatorType*> M;

            M.resize(maxLevel);

            for (int i=0; i<maxLevel; ++i)
                M[i] = &(const_cast<typename TransferOperator::TransferOperatorType&>(T[i].getMatrix()));
            assembleMatrixHierarchy(M);
        }

        template <class TransferOperator, class RealTransferOperator>
        void assembleDerivedOperatorPointerHierarchy(std::vector<TransferOperator*>& T) const
        {
            typedef typename RealTransferOperator::TransferOperatorType TransferOperatorType;
            std::vector <TransferOperatorType*> M;

            M.resize(maxLevel);

            for (int i=0; i<maxLevel; ++i)
            {
                RealTransferOperator* t = dynamic_cast<RealTransferOperator*>(T[i]);
                M[i] = &(const_cast<TransferOperatorType&>(t->getMatrix()));
            }
            assembleMatrixHierarchy(M);
        }

        template <class TransferOperator>
        void assembleOperatorPointerHierarchy(std::vector<TransferOperator*>& T) const
        {
            std::vector <typename TransferOperator::TransferOperatorType*> M;

            M.resize(maxLevel);

            for (int i=0; i<maxLevel; ++i)
                M[i] = &(const_cast<typename TransferOperator::TransferOperatorType&>(T[i]->getMatrix()));
            assembleMatrixHierarchy(M);
        }

        /**
         * \brief  assemble hierarchy of transfer operators for P1 elements
         *
         * @param T std::vector of shared_ptr's to matrices for interpolation operators
         *
         * If the vector's size is smaller than maxLevel, then it is
         * filled up with newly allocated matrices.
         */
        template <class Matrix>
        void assembleMatrixHierarchy(std::vector<std::shared_ptr<Matrix> >& M) const
        {
            while(M.size() < uint(maxLevel))
                M.push_back(std::make_shared<Matrix>());

            std::vector <Matrix*> Mraw(M.size());
            for (size_t i=0; i<M.size(); ++i)
                Mraw[i] = M[i].get();

            assembleMatrixHierarchy(Mraw);
        }

        /**
         * \brief  assemble hierarchy of transfer operators for P1 elements
         *
         * @param T std::vector of pointers to matrices for interpolation operators
         *
         * The vector is required to have maxLevel entries pointing
         * to already allocated matrices.
         */
        template <class Matrix>
        void assembleMatrixHierarchy(std::vector<Matrix*>& T) const
        {
            typedef std::map<int, double> LinearCombination;
            typedef std::vector<LinearCombination> BaseTransformation;
            typedef std::vector<BaseTransformation> TransformationHierarchy;
            typedef typename MultilevelBasis<GridType>::LocalFiniteElement LFE;
            typedef typename LFE::Traits::LocalBasisType::Traits::RangeType FERange;

            Dune::Timer timer;

            MultilevelBasis<GridType> multiLevelBasis(grid);
#ifdef FE_VERBOSE
            std::cout << "FE:" << "Id -> index maps build in " << timer.elapsed() << " seconds." << std::endl;
#endif


            TransformationHierarchy transformationHierarchy(maxLevel);
            for (int level=0; level<maxLevel; ++level)
                transformationHierarchy[level].resize(multiLevelBasis.size(level+1));

            // set all nodes as not processed
            std::vector< Dune::BitSetVector<1> > processed(maxLevel+1);
            for (int level=0; level<=maxLevel; ++level)
                processed[level].resize(multiLevelBasis.size(level), false);

            // loop over all levels
            timer.reset();
            for(int level=0; level<maxLevel; ++level)
            {
                // loop over all elements of current level
                for (const auto& cIt : elements(levelGridView(level)))
                {
                    const LFE& coarseFE = multiLevelBasis.getLocalFiniteElement(cIt);

                    // if element is leaf the transfer to the next level is locally the identity
                    if (cIt.isLeaf())
                    {
                        for (int coarseLevel=level; coarseLevel<maxLevel; ++coarseLevel)
                        {
                            int fineLevel = coarseLevel+1;

                            for(size_t j=0; j<coarseFE.localBasis().size(); ++j)
                            {
                                int fineIndex = multiLevelBasis.index(cIt, j, fineLevel);

                                // visit each child node only once
                                if (processed[fineLevel][fineIndex][0])
                                    continue;

                                int coarseIndex = multiLevelBasis.index(cIt, j, coarseLevel);
                                transformationHierarchy[coarseLevel][fineIndex][coarseIndex] = 1.0;
                                processed[fineLevel][fineIndex][0] = true;
                            }
                        }
                    }
                    else
                    {
                        int coarseLevel = level;
                        int fineLevel = level+1;

                        // store coarse node indices since we need them often
                        std::vector<int> coarseIndex(coarseFE.localBasis().size());
                        for(size_t i=0; i<coarseFE.localBasis().size(); ++i)
                            coarseIndex[i] = multiLevelBasis.index(cIt, i, coarseLevel);

                        std::vector<FERange> valuesAtPosition(coarseFE.localBasis().size());

                        // loop over all children on next level
                        for (const auto& fIt : descendantElements(cIt,level+1))
                        {
                            const LFE& fineFE = multiLevelBasis.getLocalFiniteElement(fIt);

                            // we need the refrence element to get the local position of the subentities corresponding to fine basis functions
                            auto fineRefElement = Dune::ReferenceElements<double, dim>::general(fIt.type());

                            // loop over all child nodes
                            for(size_t j=0; j<fineFE.localBasis().size(); ++j)
                            {
                                int fineIndex = multiLevelBasis.index(fIt, j, fineLevel);

                                // visit each child node only once
                                if (processed[fineLevel][fineIndex][0])
                                    continue;

                                // get local coordinates of subentity in fine element
                                const Dune::LocalKey& localKey = fineFE.localCoefficients().localKey(j);
                                auto localPositionFine = fineRefElement.position(localKey.subEntity(), localKey.codim());

                                // compute local coordinates of subentity in coarse element
                                auto localPositionCoarse = fIt.geometryInFather().global(localPositionFine);

                                // evaluate coarse basis functions at the position of the subentity corresponding to the fine basis function
                                coarseFE.localBasis().evaluateFunction(localPositionCoarse, valuesAtPosition);

                                for(size_t i=0; i<coarseFE.localBasis().size(); ++i)
                                {
                                    if (valuesAtPosition[i] > 1e-5)
                                        transformationHierarchy[coarseLevel][fineIndex][coarseIndex[i]] = valuesAtPosition[i];
                                }

                                processed[fineLevel][fineIndex][0] = true;
                            } // loop over all child nodes
                        } // end of loop over all children on next level
                    }
                } // end of loop over all elements of current level
            } // end of loop over all levels
#ifdef FE_VERBOSE
            std::cout << "FE:" << "Grid traversed for transfer operators in " << timer.elapsed() << " seconds." << std::endl; 
#endif

            // setup transfer operator matrices
            timer.reset();
            //  T.resize(maxLevel);
            for(int level=0; level<maxLevel; ++level)
            {
                Dune::MatrixIndexSet indices(multiLevelBasis.size(level+1), multiLevelBasis.size(level));

                for(size_t row=0; row<transformationHierarchy[level].size(); ++row)
                    for(const auto& colIt : transformationHierarchy[level][row])
                        indices.add(row,colIt.first);

                indices.exportIdx(*T[level]);

                for(size_t row=0; row<transformationHierarchy[level].size(); ++row)
                {
                    for(const auto& colIt : transformationHierarchy[level][row])
                    {
                        //                if (colIt->second != 0.0)
                        (*T[level])[row][colIt.first] = 0.0;
                        for(size_t i=0; i<Matrix::block_type::rows; ++i)
                            (*T[level])[row][colIt.first][i][i] = colIt.second;
                    }
                }

                transformationHierarchy[level].clear();
            }

#ifdef FE_VERBOSE
            for(int level=0; level<maxLevel; ++level)
                std::cout << "FE:" << "Transfer " << level << " -> " << level+1 << " is a "<< (*T[level]).N() << " x " << (*T[level]).M() << " matrix." << std::endl;
            std::cout << "FE:" << "Transfer operator matrices set up in " << timer.elapsed() << " seconds." << std::endl;
#endif
        }


    private:
        static const int dim = GridType::dimension;
        const GridType& grid;
        int maxLevel;
};

#endif
