The `Image` class contains only a couple members, including a place to store the grayscale image as well as the file name of the photo imported. Instatiating the class will read the file provided in the constructor and import the data from that location.

Image has a few member functions `Save()`, `Convolution()`, `BoxBlur()`, and `Sharpness()`. The `Save()` member takes in a file name to save the current image to. I have chosen that every member function affects the current state of the `Image` instance. That is to say, applying `BoxBlur()` will change the current image to a blurred version. The `Convolution()` member function is a general function to apply a kernel to an image, which both `BoxBlur()` and `Sharpness()` take advantage of by providing their own custom kernels.

The `Convolution()` member function has some important behaviors to point out. This function does element by element multiplication of a kernel and a block surounding a pixel on an image. Because the image consists of a 2D array of `unsigned char` the maximum value is only `255`. That being the case, the intermediate summation is done with a `double` type variable. In general, this will have to be rounded to the closest `unsigned char` value. That being the case, we actually choose to take the `floor()` of the sum and then cast to `unsigned char`. Before this, we check if the sum is negative, in which case we simply set the value to zero (since the `char` is `unsigned`).

Doing this, and following the directions given, we obtain identical output as what the HW pdf reports.

```
/home/jbarnett/Drive/School/Stanford/Fall19/CME211/hw6/cmake-build-debug/main
Origional Image: 255
BoxBlur( 3): 139
BoxBlur( 7): 44
BoxBlur(11): 27
BoxBlur(15): 21
BoxBlur(19): 16
BoxBlur(23): 11
BoxBlur(27): 9
```
