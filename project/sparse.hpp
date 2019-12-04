#ifndef SPARSE_HPP
#define SPARSE_HPP

#include <vector>
#include <tuple>

class SparseMatrix
{
  private:
    std::vector<int> i_idx;
    std::vector<int> j_idx;
    std::vector<double> a;
    int ncols;
    int nrows;
    bool isCSR = false;


  public:

    /* Method to modify sparse matrix dimensions */
    void Resize(int nrows, int ncols);

    /* Method to add entry to matrix in COO format */
    void AddEntry(int i, int j, double val);

    /* Method to convert COO matrix to CSR format using provided function */
    void ConvertToCSR();

    /* Method to perform sparse matrix vector multiplication using CSR formatted matrix */
    std::vector<double> MulVec(std::vector<double> &vec);

    /**
     * Defines a GEMM operation given as alpha*M*b + beta*c
     * @param alpha constant to multiply A*b
     * @param beta constant to multiply c
     * @param M Sparse matrix in equation
     * @param b Vector multiplied in alpha*A*b
     * @param c Constant vector to add to result
     * @return alpha*A*b + c
     */
    friend std::vector<double> CSR_GEMM(double alpha,
                                        double beta,
                                        const SparseMatrix &M,
                                        const std::vector<double> &b,
                                        const std::vector<double> &c);
    
};

#endif /* SPARSE_HPP */
