//
// Created by jbarnett8 on 11/12/19.
//

#ifndef PROJECT_MATVECOPS_H
#define PROJECT_MATVECOPS_H

#include <vector>

/**
 * A simple L2-Norm implementation
 * @param vec The vector to find norm
 * @return the norm
 */
double l2norm(std::vector<double> &vec);

/**
 * Perform a dot product between two vectors of equal length
 * @param l The first vector
 * @param r The second vector
 * @return The scalar value giving the dot product
 */
double dot(std::vector<double> &l, std::vector<double> &r);

/**
 * Calculate the general expression d = alpha * x + beta * y element
 * by element
 * @param alpha The scalar constant in front of x
 * @param x The vector to be added
 * @param beta The scalar constant in front of y
 * @param y The vector to be added
 * @return The vector sum
 */
std::vector<double> axby(double alpha, std::vector<double> &x,
                         double beta, std::vector<double> &y);

/**
 * Defines a GEMM operation given as alpha*A*b + beta*c
 * @param alpha constant to multiply A*b
 * @param beta constant to multiply c
 * @param v_vec values in CSR matrix A
 * @param r_vec row pointers in CSR matrix A
 * @param c_vec column indices in CSR matrix A
 * @param b Vector multipled in alpha*A*b
 * @param c Constant vector to add to result
 * @return alpha*A*b + c
 */
std::vector<double> GEMM(double alpha,
                         double beta,
                         const std::vector<double> &v_vec,
                         const std::vector<int> &r_vec,
                         const std::vector<int> &c_vec,
                         const std::vector<double> &b,
                         const std::vector<double> &c);

#endif //PROJECT_MATVECOPS_H
