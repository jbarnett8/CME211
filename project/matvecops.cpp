//
// Created by jbarnett8 on 11/12/19.
//

#include <cassert>
#include <cmath>

#include "matvecops.hpp"

double l2norm(std::vector<double> &vec) {
    double norm = 0;
    for (const auto &v: vec)
        norm += v * v;
    return sqrt(norm);
}

double dot(std::vector<double> &l, std::vector<double> &r) {
    double val = 0;
    for (unsigned i = 0; i < l.size(); i++) {
        val += l[i] * r[i];
    }
    return val;
}

std::vector<double> axby(double alpha, std::vector<double> &x,
                         double beta, std::vector<double> &y) {
    assert(x.size() == y.size());
    std::vector<double> ret_vec(x.size(), 0);
    for (unsigned i = 0; i < x.size(); i++) {
        ret_vec[i] = alpha * x[i] + beta * y[i];
    }

    return ret_vec;
}


std::vector<double> GEMM(double alpha,
                         double beta,
                         const std::vector<double> &v_vec,
                         const std::vector<int> &r_vec,
                         const std::vector<int> &c_vec,
                         const std::vector<double> &b,
                         const std::vector<double> &c) {
    // Declare our vector to return
    std::vector<double> ret_vec(b.size(), 0);

    // We iterate through each item in the return vector
    for (unsigned i = 0; i < ret_vec.size(); i++) {

        // We get the range from the row pointers
        auto start = r_vec[i], stop = r_vec[i + 1];

        // These inform the range for j and the column vector
        for (auto j = start; j < stop; j++) {
            ret_vec[i] += alpha * v_vec[j] * b[c_vec[j]];
        }
        ret_vec[i] += beta * c[i];
    }
    return ret_vec;
}
