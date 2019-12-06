#include <vector>
#include <string>


class Stock {
    private:

    /* private member variables */
    std::vector<double> prices, daily_ret;
    std::string stock_ticker;
    double mean_return, var_return;
    bool mean_calced, var_calced;

    public:

    //constructor
    Stock( std::vector<double> price_vec, std::string tckr);

    //calculate daily return
    std::vector<double> dailyReturn();

    //calculate mean return
    double meanReturn();

    //calculate return variance
    double varReturn();

    // Simply gives the stock name (in case lost upstream by user)
    // We define in-place because of its simplicity
    std::string ticker() { return stock_ticker; }

};
