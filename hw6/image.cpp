//
// Created by jbarnett8 on 11/21/19.
//

#include <boost/multi_array.hpp>
#include <jpeglib.h>
#include <iostream>
#include <cassert>
#include <iomanip>
#include <limits>

#include "image.hpp"
#include "hw6.hpp"

Image::Image(const std::string &file_name) {
    og_file_name = file_name;
    ReadGrayscaleJPEG(file_name, img);
}

void Image::Save(std::string &file_name) {
    if (file_name.empty())
        WriteGrayscaleJPEG(og_file_name, img);
    else
        WriteGrayscaleJPEG(file_name, img);
}

void Image::Convolution(const boost::multi_array<unsigned char, 2> &input,
                        boost::multi_array<unsigned char, 2> &output,
                        boost::multi_array<float, 2> &kernel) {
    auto dims = input.shape(), o_dims = output.shape(), k_dims = kernel.shape();
    assert(k_dims[0] == k_dims[1]);
    auto rows = static_cast<int>(dims[0]), cols = static_cast<int>(dims[1]),
            k_n = static_cast<int>(k_dims[0]);

    if ((k_n < 3) || ((k_n % 2) == 0) || (k_dims[0] != k_dims[1])) {
        std::cerr << "The kernel is not the proper size. Must be at least 3, "
                  << "odd, and square. " << std::endl;
        std::exit(1);
    }

    if ((dims[0] != o_dims[0]) || (dims[1] != o_dims[1])) {
        std::cerr << "The input and output image sizes do not match. "
                  << std::endl;
        std::exit(1);
    }

    auto k_mid = k_n / 2;
    auto uc_max = std::numeric_limits<unsigned char>::max();

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            double sum = 0;
            for (int k_i = -k_mid; k_i <= k_mid; k_i++)
                for (int k_j = -k_mid; k_j <= k_mid; k_j++) {
                    auto ii = i + k_i;
                    ii = ii >= 0 ? ii : 0;
                    ii = ii < rows ? ii : rows - 1;
                    auto jj = j + k_j;
                    jj = jj >= 0 ? jj : 0;
                    jj = jj < cols ? jj : cols - 1;
                    sum += (kernel[k_i + k_mid][k_j + k_mid] *
                            static_cast<double>(input[ii][jj]));
                }
            sum = sum > 0 ? sum : 0;
            sum = sum < uc_max ? sum : uc_max;
            output[i][j] = static_cast<unsigned char>(floor(sum));
        }
    }
}

void Image::BoxBlur(unsigned n) {
    boost::multi_array<float, 2> kernel(boost::extents[n][n]);
    auto normalize = static_cast<float>(pow(n, 2.0));
    for (unsigned i = 0; i < n; i++)
        for (unsigned j = 0; j < n; j++)
            kernel[i][j] = 1.0f/normalize;
    auto img_write = img;
    Convolution(img, img_write, kernel);
    img = img_write;
}

unsigned Image::Sharpness() {
    const unsigned n = 3;
    float d_kernel[n][n] = {{0, 1, 0}, {1, -4, 1}, {0, 1, 0}};
    boost::multi_array<float, 2> kernel(boost::extents[n][n]);
    for (unsigned i = 0; i < n; i++)
        for (unsigned j = 0; j < n; j++)
            kernel[i][j] = d_kernel[i][j];
    auto img_write = img;
    Convolution(img, img_write, kernel);
    auto dims = img.shape();
    auto rows = dims[0], cols = dims[1];
    unsigned char max = 0;
    for (unsigned i = 0; i < rows; i++)
        for (unsigned j = 0; j < cols; j++)
            max = img_write[i][j] > max ? img_write[i][j] : max;
    return static_cast<unsigned>(max);
}