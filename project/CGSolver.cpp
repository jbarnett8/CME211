//
// Created by jbarnett8 on 11/12/19.
//

#include <iostream>
#include <fstream>
#include <iomanip>

#include "CGSolver.hpp"
#include "matvecops.hpp"
#include "sparse.hpp"


int CGSolver(SparseMatrix        &M,
             std::vector<double> &b,
             std::vector<double> &x,
             double tol,
             unsigned n_max) {

    // The GEMM function sometimes needs a zero vector
    std::vector<double> zero(b.size(), 0);

    // Calculate the first r vector
    auto rn = CSR_GEMM(-1, 1, M, x, b);

    // We store the current solution here
    std::vector<double> un(b.size());
    std::copy(x.begin(), x.end(), un.begin());

    auto l2r0 = l2norm(rn);
    auto pn = rn;
    unsigned n = 0;
    while (n < n_max) {
        n++;
        // Calc A * p
        auto Ap = CSR_GEMM(1, 1, M, pn, zero);
        // Calc (rn.rn)/(pn^T.A.pn)
        double alpha = dot(rn, rn) / dot(pn, Ap);
        // Calc un + alpha * pn
        auto unp1 = axby(1, un, alpha, pn);
        // Calc -A * pn + pn
        auto rnp1 = CSR_GEMM(-alpha, 1, M, pn, rn);
        if ((l2norm(rnp1) / l2r0) < tol) {
            // If we get to our desired tolerance, we copy solution to x and
            // return num iterations
            std::copy(unp1.begin(), unp1.end(), x.begin());
            return n;
        }
        // Calculate beta and next iterates
        double beta = dot(rnp1, rnp1) / dot(rn, rn);
        pn = axby(1, rnp1, beta, pn);
        rn = rnp1;
        un = unp1;
    }
    // failure state
    std::copy(un.begin(), un.end(), x.begin());
    return -1;
}