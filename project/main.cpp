//
// Created by jbarnett8 on 11/18/19.
//

#include <fstream>
#include <iomanip>
#include <iostream>

#include "CGSolver.hpp"
#include "COO2CSR.hpp"

void print_help();

int main(int argc, char *argv[]) {

    // Simple check that we have the right # of arguments
    if (argc != 3) {
        std::cout << "Incorrect number of program arguments." << std::endl;
        print_help();
        std::exit(1);
    }

    // Declaring storage for reading/writing files, then opening
    std::string line;
    std::ifstream mat(argv[1]);
    std::ofstream sol(argv[2]);
    unsigned rows, cols;
    std::vector<int> r_vec, c_vec;
    std::vector<double> v_vec;

    // Make sure we actually opened the files
    if (mat.is_open()) {

        // Get the first line, then grab the values
        mat >> rows >> cols;
        int r, c;
        double v;
        while (mat >> r >> c >> v) {
            r_vec.push_back(r);
            c_vec.push_back(c);
            v_vec.push_back(v);
        }

        mat.close();

    } else {
        std::cout << "couldn't open matrix file" << std::endl;
        print_help();
        exit(1);
    }

    // Convert matrix type
    COO2CSR(v_vec, r_vec, c_vec);

    r_vec.resize(rows + 1);
    std::vector<double> b(cols, 0), u(cols, 1);

    // Call our solver and get the return state
    auto state = CGSolver(v_vec, r_vec, c_vec, b, u, 1E-5);
    if (state < 0) {
        std::cout << "FAILURE" << std::endl;
        exit(1);
    } else {
        std::cout << "SUCCESS: CG solver converged in " << state
                  << " iterations." << std::endl;
    }

    if (sol.is_open()) {
        sol << std::setprecision(4) << std::scientific;
        for (auto &v : u)
            sol << v << std::endl;
    } else {
        std::cout << "couldn't open solution file for writing" << std::endl;
        print_help();
        exit(1);
    }
}

void print_help() {
    std::cout << "CG Solver takes in a file representing a matrix and outputs"
              << " a heat equation solution" << std::endl;
    std::cout << "matrix file: \t name of the file containing matrix data"
              << std::endl;
    std::cout << "solution file: \t name of the file to write solution"
              << std::endl;
}
