#ifndef HEAT_HPP
#define HEAT_HPP

#include <string>
#include <vector>

#include "sparse.hpp"

class HeatEquation2D
{
  private:
    SparseMatrix A;
    std::vector<double> b, x;
    double length, width, h, T_h, T_c;
    int n_r, n_c;
    const unsigned max_n = 1000;

    void print_soln(std::string fname);
    double calc_jet_temp(double x);
    static bool CGIterate(SparseMatrix &M,
                          std::vector<double> &b,
                          std::vector<double> &x,
                          std::vector<double> &rn,
                          std::vector<double> &pn,
                          double l2r0,
                          double tol);

  public:
    /* Method to setup Ax=b system */
    int Setup(std::string inputfile);

    /* Method to solve system using CGsolver */
    int Solve(std::string soln_prefix);

};

#endif /* HEAT_HPP */
