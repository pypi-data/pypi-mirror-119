// -*- tab-width: 8; indent-tabs-mode: nil; c-basic-offset: 4 -*-
// vi: set et ts=8 sw=4 sts=4:

#include <cmath>
#include <limits>
#include <iostream>
#include <iomanip>
#include <dune/solvers/solvers/solver.hh>

template <class VectorType, class BitVectorType>
void Dune::Solvers::LoopSolver<VectorType, BitVectorType>::preprocess()
{
    this->iterationStep_->preprocess();
}

template <class VectorType, class BitVectorType>
void Dune::Solvers::LoopSolver<VectorType, BitVectorType>::solve()
{

    int i;

    // Check whether the solver is set up properly
    this->check();

    if (this->verbosity_ != NumProc::QUIET)
        std::cout << "--- LoopSolver ---\n";

    if (this->verbosity_ == NumProc::FULL)
    {
        std::cout << " iter";
        if (referenceSolution_)
        {
            if (this->useRelativeError_)
                std::cout << "          error";
            std::cout << "      abs error";
            std::cout << " abs correction";
        }
        else
        {
            if (this->useRelativeError_)
                std::cout << "     correction";
            std::cout << " abs correction";
        }
        std::cout << "     rate";
        std::string header = this->iterationStep_->getOutput();
        std::cout << header;

        for(auto&& c: criteria_)
            std::cout << c.header();


        std::cout << std::endl;

        std::cout << "-----";
        if (this->useRelativeError_)
            std::cout << "---------------";
        if (referenceSolution_)
            std::cout << "---------------";
        std::cout << "---------------";
        std::cout << "---------";
        for(size_t i=0; i<header.size(); ++i)
            std::cout << "-";

        for(auto&& c: criteria_)
            std::cout << std::string(c.header().size(), '-');

        std::cout << std::endl;
    }

    real_type error = std::numeric_limits<real_type>::max();

    real_type normOfOldCorrection = 1;
    real_type normOfOldError = 0;
    real_type totalConvRate = 1;
    this->maxTotalConvRate_ = 0;
    int convRateCounter = 0;

    // Loop until desired tolerance or maximum number of iterations is reached
    for (i=0; i<this->maxIterations_ && (error>this->tolerance_ || std::isnan(error)); i++)
    {
        iter_ = i;

        // Backup of the current solution for the error computation later on
        VectorType oldSolution = this->iterationStep_->getSol();

        // Perform one iteration step
        this->iterationStep_->iterate();

        // write iteration to file, if requested
        if (this->historyBuffer_!="")
            this->writeIterate(this->iterationStep_->getSol(), i);

        // Compute error
        real_type oldNorm = this->errorNorm_->operator()(oldSolution);

        real_type normOfError=std::numeric_limits<real_type>::quiet_NaN();

        // Please don't replace this call to 'diff' by computing the norm of the difference.
        // In some nonlinear DD applications the 'diff' method may be nonlinear.
        real_type normOfCorrection = this->errorNorm_->diff(oldSolution,this->iterationStep_->getSol());
        convRate_ = (normOfOldCorrection > 0)
            ? normOfCorrection / normOfOldCorrection : 0.0;
        error = normOfCorrection;
        normOfOldCorrection = normOfCorrection;

        // If a reference solution has been provided compute the error with respect to it
        if (referenceSolution_)
        {
            normOfError = this->errorNorm_->diff(this->iterationStep_->getSol(), *referenceSolution_);
            convRate_ = (normOfOldError > 0) ? normOfError / normOfOldError : 0.0;
            error = normOfError;
            normOfOldError = normOfError;
        }

        // Turn the error into the relative error, if requested
        if (this->useRelativeError_ && error != 0)
            error = (oldNorm == 0) ? std::numeric_limits<real_type>::max()
                                   : error / oldNorm;

        if (!std::isinf(convRate_) && !std::isnan(convRate_) && i>0)
        {
            totalConvRate *= convRate_;
            this->maxTotalConvRate_ = std::max(this->maxTotalConvRate_, std::pow(totalConvRate, 1/((real_type)convRateCounter+1)));
            convRateCounter++;
        }

        // Output
        bool stop = false;
        if (this->verbosity_ == NumProc::FULL) {
            std::streamsize const oldPrecision = std::cout.precision();
            std::ios_base::fmtflags const oldFormatFlags = std::cout.flags();

            std::cout << std::setw(5) << i;

            if (this->useRelativeError_)
            {
                std::cout << std::scientific
                          << std::setw(15) << std::setprecision(7) << error;
            }

            if (referenceSolution_)
            {
                std::cout << std::scientific
                          << std::setw(15) << std::setprecision(7) << normOfError;
            }

            std::cout << std::scientific
                      << std::setw(15) << std::setprecision(7) << normOfCorrection;

            if (i == 0)
                // We can't estimate the convergence rate at the first iteration
                std::cout << "         ";
            else
                std::cout << std::fixed
                          << std::setw(9) << std::setprecision(5) << convRate_;

            std::cout << std::setprecision(oldPrecision);
            std::cout.flags(oldFormatFlags);

            std::cout << this->iterationStep_->getOutput();

            for(auto&& c: criteria_)
            {
                auto r = c();
                stop = stop or std::get<0>(r);
                std::cout << std::get<1>(r);
            }

            std::cout << std::endl;

        }
        else
        {
            for(auto&& c: criteria_)
                stop = stop or std::get<0>(c());
        }
        if (stop)
            break;
    }


    if (this->verbosity_ != NumProc::QUIET) {
        std::cout << "maxTotalConvRate: " << this->maxTotalConvRate_ << ",   "
                  << i << " iterations performed\n";
        std::cout << "--------------------\n";
    }

    this->setResult(i,error<=this->tolerance_,totalConvRate);

}
