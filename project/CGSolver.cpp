//
// Created by jbarnett8 on 11/12/19.
//

#include <iostream>
#include <fstream>
#include <iomanip>

#include "CGSolver.hpp"
#include "matvecops.hpp"


int CGSolver(std::vector<double> &val,
             std::vector<int> &row_ptr,
             std::vector<int> &col_idx,
             std::vector<double> &b,
             std::vector<double> &x,
             double tol) {

    // The GEMM function sometimes needs a zero vector
    std::vector<double> zero(b.size(), 0);

    // Calculate the first r vector
    auto rn = GEMM(-1, 1, val, row_ptr, col_idx, x, b);

    // We store the current solution here
    std::vector<double> un(b.size());
    std::copy(x.begin(), x.end(), un.begin());

    auto l2r0 = l2norm(rn);
    auto pn = rn;
    unsigned n = 0, max_n = 1000;
    while (n < max_n) {
        n++;
        // Calc A * p
        auto Ap = GEMM(1, 1, val, row_ptr, col_idx, pn, zero);
        // Calc (rn.rn)/(pn^T.A.pn)
        double alpha = dot(rn, rn) / dot(pn, Ap);
        // Calc un + alpha * pn
        auto unp1 = axby(1, un, alpha, pn);
        // Calc -A * pn + pn
        auto rnp1 = GEMM(-alpha, 1, val, row_ptr, col_idx, pn, rn);
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
    return -1;
}