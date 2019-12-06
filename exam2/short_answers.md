# Short Answer Questions

## Section 1.1

(A) Selection (3) there are no problems is the proper response. We are simply asigning values of one `int` primitive type members from another, and there is not even any implicit type conversion.

(B) Selection (2) the snippet will likely result in a crash. The syntax for the assignment operation to the `double[][]` type is correct, but it assigns outside of the memory allocated in the stack.

(C) Selection (3) there are no problems. The synatx for selecting a value from the array is correct and the types between source and assignment are the same.

(D) Selection (1) it will not compile. The redeclaration of the member `n` is not allowed (even if it was the same type) and the compiler will complain.

(E) The `unsigned char` has 8 bits and is assigned to its maximum value. This means the representation of `255` is in binary `11111111`. Incremeneting this number by one will result in catastropic overflow since the addition will carry over to the entire number, which results in `00000000` which is the representation of 0.

(F) The finite precision representation of numbers along with the non-linear distribution of floating-point numbers makes it necessary to consider the effects of numerical underflow/overflow and ill-conditioning. In the case of two small numbers being multiplied, it is possible for numerical underflow to occur where the result of the product will actually result in undefined behavior (depending on the language specifications). A potential remedy is to first normalize these values based on the sum of the two numbers (which are non-negative because they represent probabilities). This will bring the floating point representation to 0 where we have the densest representation of floating point values.

## Section 1.2

(A) Stack allocation occurs at compile time while heap allocation occurs during runtime, and stack space is typically much smaller than memory available in the heap.

(B) We observe different values because the `int triplet[3]` is declared on the stack out of scope of the `main()` function, so upon returning the value for the `int*` referenced at the second element is undefined.

(C) This corrects the issue because we are now declaring the variable on the heap which will allocate new memory for the result for every call to the function `make_triplet` which will not go out of scope in `main()` and will persist until `delete` is called. 

(D) Yes. Because every call of `make_triplet` calls `new`, new memory is allocated every time. There are no assocated `delete` calls in the `main` program, so this will quickly result in the system running out of memory if unchecked.

(E) Returning a `std::vector<int>` instead will result in proper memory management since these standard library objects relieve us of the duty to perform garbage collection manually. When the variable goes out of scope, the space will be automatically freed for us.