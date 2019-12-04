//
// Created by jbarnett8 on 11/25/19.
//

#include <iostream>
#include <algorithm>

#include "COO2CSR.hpp"
#include "matvecops.hpp"
#include "sparse.hpp"

void SparseMatrix::Resize(int nrows, int ncols) {
    if (!j_idx.empty()) {
        int max_col = *std::max_element(j_idx.begin(), j_idx.end()) + 1;
        auto max_row = static_cast<int>(i_idx.size());
        if ((max_row > nrows) || (max_col > ncols))
            throw std::runtime_error("Matrix resize is invalid.");
    }
    this->nrows = nrows;
    this->ncols = ncols;
}

void SparseMatrix::AddEntry(int i, int j, double val) {
    if (!isCSR) {
        this->i_idx.push_back(i);
        this->j_idx.push_back(j);
        this->a.push_back(val);
    } else {
        throw std::runtime_error("Cannot add entry to CSR matrix.");
    }
}

void SparseMatrix::ConvertToCSR() {
    COO2CSR(this->a, this->i_idx, this->j_idx);
    isCSR = true;
}

std::vector<double> SparseMatrix::MulVec(std::vector<double> &vec) {
    if (!isCSR) {
        throw std::runtime_error("code does not support non-CSR matrix mult.");
    }

    // Declare our vector to return
    std::vector<double> ret_vec(vec.size(), 0);

    // We iterate through each item in the return vector
    for (unsigned long i = 0; i < ret_vec.size(); i++) {

        // We get the range from the row pointers
        auto start = i_idx[i], stop = i_idx[i + 1];

        // These inform the range for j and the column vector
        for (auto j = start; j < stop; j++) {
            ret_vec[i] += this->a[j] * vec[j_idx[j]];
        }
    }
    return ret_vec;
}

std::vector<double> CSR_GEMM(double alpha,
                             double beta,
                             const SparseMatrix &M,
                             const std::vector<double> &b,
                             const std::vector<double> &c) {
    return GEMM(alpha, beta, M.a, M.i_idx, M.j_idx, b, c);
}
