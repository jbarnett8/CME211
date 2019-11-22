//
// Created by jbarnett8 on 11/21/19.
//

#ifndef HW6_IMAGE_H
#define HW6_IMAGE_H

class Image {

public:
    explicit Image(const std::string &file_name);

    void Save(std::string &file_name);

    void Convolution(const boost::multi_array<unsigned char, 2> &input,
                     boost::multi_array<unsigned char, 2> &output,
                     boost::multi_array<float, 2> &kernel);

    /**
     * Blurs the image provided using a kernel of size n
     * @param n The size of the kernel
     */
    void BoxBlur(unsigned n);

    /**
     * Measures the sharpness of an image -- gives maximum value
     */
    unsigned Sharpness();

private:
    boost::multi_array<unsigned char, 2> img;
    std::string og_file_name;
};

#endif //HW6_IMAGE_H
