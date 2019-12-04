//
// Created by jbarnett on 12/1/19.
//

#include "heat.hpp"
#include "sparse.hpp"
#include "CGSolver.hpp"
#include "matvecops.hpp"

#include <iostream>
#include <fstream>
#include <cmath>
#include <algorithm>
#include <sstream>
#include <iomanip>

int HeatEquation2D::Setup(std::string inputfile) {
    std::ifstream infile(inputfile);

    // Make sure we actually opened the files
    if (infile.is_open()) {

        // Get the values from the file
        infile >> length >> width >> h >> T_c >> T_h;
        infile.close();

        // Package up the variables and check if they're valid
        auto vals = {length, width, h, T_c, T_h};
        bool invalid_vals = false;
        for (auto &v : vals)
            if (std::isnan(v)) {
                invalid_vals = true;
            }
        // Wrap up the checks in one if statement
        if ((length < 0) || (width < 0) || (h < 0) ||invalid_vals) {
            throw std::runtime_error(
                    "One of the inputs is invalid. Check input file.");
        }
    } else {
        throw std::runtime_error("Failed to open input file");
    }

    // We set the size of the matrix, keeping in mind that the width will have extra points to evaluate
    n_c = static_cast<int>(length/h);
    n_r = static_cast<int>(width/h) - 1;
    A.Resize(n_c*n_r, n_c*n_r);

    // Make a new b vector to set all elements to zero, copy to real b later
    std::vector<double> bb(static_cast<std::size_t>(n_c*n_r), 0);
    double hh = 1; //h*h;
    for (int i = 0; i < n_r; i++) {
        for (int j = 0; j < n_c; j++) {
            auto idx = i*n_c + j;
            A.AddEntry(idx, idx, -4);

            if (i == 0) bb[idx] -= hh*T_h;
            else A.AddEntry(idx, idx - n_c, 1);

            if (i == (n_r - 1))
                bb[idx] -= hh*calc_jet_temp(j * h);
            else A.AddEntry(idx, idx + n_c, 1);

            if (j == 0) A.AddEntry(idx, idx + n_c - 1, 1);
            else A.AddEntry(idx, idx - 1, 1);

            if (j == (n_c - 1)) A.AddEntry(idx, idx - n_c + 1, 1);
            else A.AddEntry(idx, idx + 1, 1);
        }
    }
    b.resize(static_cast<unsigned>(n_c*n_r));
    std::copy(bb.begin(), bb.end(), b.begin());

    A.ConvertToCSR();

    return 0;
}

int HeatEquation2D::Solve(std::string soln_prefix) {
    // We start with a vector of ones as the trial solution
    x.resize(static_cast<unsigned>(n_c*n_r));
    for (auto &val : x)
        val = 1;
    unsigned n = 0, increment = 10;
    bool state = true;
    // Calculate the first r vector and setup other variables
    auto rn = CSR_GEMM(-1, 1, A, x, b);
    auto l2r0 = l2norm(rn);
    auto pn = rn;

    bool success;
    do {
        if ((n % increment) == 0) {
            std::stringstream fname;
            fname << soln_prefix << std::setfill('0') << std::setw(3) << n << ".txt";
            print_soln(fname.str());
        }
        success = CGIterate(A, b, x, rn, pn, l2r0, 1E-5);
        if (success)
            state = false;
        if (n > max_n)
            state = false;
        n++;
    } while (state);

    auto fname = soln_prefix + std::to_string(n) + ".txt";
    print_soln(fname);
    if (success) {
        std::cout << "SUCCESS: CG Solver converged in " << std::setw(2) << n << " iterations." << std::endl;
    } else {
        std::cout << "FAILURE: CG Solver reached maximum number of iterations and did not converge." << std::endl;
    }
    return 0;
}

double HeatEquation2D::calc_jet_temp(double x) {
    return -T_c*(exp(-10*pow(x - length/2, 2)) - 2);
}

void HeatEquation2D::print_soln(std::string fname) {
    std::ofstream f;
    f.open(fname);
    if (f.is_open()) {
        for (int j = 0; j < n_c + 1; j++)
            f << T_h << " ";
        f << std::endl;
        for (int i = 0; i < n_r; i++) {
            for (int j = 0; j < n_c; j++) {
                auto idx = i*n_c + j;
                f << x[idx] << " ";
            }
            f << x[i*n_c] << std::endl;
        }
        for (int j = 0; j < n_c; j++)
            f << calc_jet_temp(j*h) << " ";
        f << calc_jet_temp(0) << std::endl;
        f.close();
    } else {
        throw std::runtime_error("error opening solution file for writing");
    }
}

bool HeatEquation2D::CGIterate(SparseMatrix &M,
                               std::vector<double> &b,
                               std::vector<double> &x,
                               std::vector<double> &rn,
                               std::vector<double> &pn,
                               double l2r0,
                               double tol) {
    std::vector<double> zero(b.size(), 0);
    // Calc A * p
    auto Ap = CSR_GEMM(1, 1, M, pn, zero);
    // Calc (rn.rn)/(pn^T.A.pn)
    double alpha = dot(rn, rn) / dot(pn, Ap);
    // Calc un + alpha * pn
    auto unp1 = axby(1, x, alpha, pn);
    // Calc -A * pn + pn
    auto rnp1 = CSR_GEMM(-alpha, 1, M, pn, rn);
    if ((l2norm(rnp1) / l2r0) < tol) {
        // If we get to our desired tolerance, we copy solution to x and
        // return num iterations
        std::copy(unp1.begin(), unp1.end(), x.begin());
        return true;
    }
    // Calculate beta and next iterates
    double beta = dot(rnp1, rnp1) / dot(rn, rn);
    pn = axby(1, rnp1, beta, pn);
    rn = rnp1;
    std::copy(unp1.begin(), unp1.end(), x.begin());
    return false;
}
