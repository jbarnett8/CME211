#include <vector>
#include <string>
#include <fstream>
#include <iostream>

#include "Stock.hpp"

void print_help_text() {
    std::cout << "This program calculates the average daily return and "
                 "variance of a particular stock." << std::endl;
    std::cout << "-----------------------------------------------------" <<
              std::endl;
    std::cout << "file name: name of text file with stock prices (must all be"
                 " non-zero values with at least 2 entries. " << std::endl;
    std::cout << "ticker name: The continous string of letters that represent"
                 " the stock ticker. " << std::endl;
}

int main(int argc, char * argv[]) {

    /* Read in command line arguments */
    if (argc != 3) {
        std::cerr << "Incorrect number of input arguments. " << std::endl;
        print_help_text();
    }

    // Grab the names
    auto price_file = std::string(argv[1]);
    auto ticker_name = std::string(argv[2]);

    // Settup variables for reading and storage
    std::ifstream in_file;
    in_file.open(price_file);
    double curr_price = 0;
    std::vector<double> prices;

    // Check that we opened the file
    if (!in_file.is_open()) {
        std::cerr << "Failed to open " << price_file << ". " << std::endl;
        print_help_text();
    }

    // Read all the numbers into the vector
    while (in_file >> curr_price)
        prices.push_back(curr_price);

    in_file.close();

    /* Call the Stock class constructor */
    Stock stock(prices, ticker_name);

    /* Perform reqired calculations */
    auto mean_return = stock.meanReturn();
    auto var_return = stock.varReturn();

    /* Write out to results.txt */
    std::ofstream out_file;
    out_file.open("results.txt");
    if (!out_file.is_open()) {
        std::cerr << "Failed to open results.txt " << std::endl;
        print_help_text();
    }
    out_file << stock.ticker() << std::endl;
    out_file << mean_return << std::endl << var_return << std::endl;
    out_file.close();

    return 0;
}

