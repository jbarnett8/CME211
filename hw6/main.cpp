//
// Created by jbarnett8 on 11/21/19.
//

#include <boost/multi_array.hpp>
#include <iomanip>
#include <iostream>
#include <string>

#include "image.hpp"

int main() {
    Image stanford("stanford.jpg");
    auto sharp = stanford.Sharpness();
    std::cout << "Origional Image: " << sharp << std::endl;

    for (unsigned n = 3; n <= 27; n += 4) {
        Image stanford_box("stanford.jpg");
        stanford_box.BoxBlur(n);
        std::stringstream f;
        f << "BoxBlur" << std::setfill('0') << std::setw(2)
          << n << ".jpg";
        auto file = f.str();
        stanford_box.Save(file);
        sharp = stanford_box.Sharpness();
        std::cout << "BoxBlur(" << std::setw(2) << n << "): "
                  << sharp << std::endl;
    }
}