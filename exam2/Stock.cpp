//
// Created by jbarnett8 on 12/5/19.
//

#include "Stock.hpp"
#include <utility>
#include <iostream>
#include <numeric>
#include <algorithm>

Stock::Stock(std::vector<double> price_vec, std::string tckr) {
    if ((price_vec.size() <= 1) || tckr.empty()) {
        throw std::runtime_error("Invalid construction of Stock. Either the "
                                 "price vector is too small (<= 1) or the "
                                 "ticker name is empty.");
    }

    // We store the values (we use move since its passing a copy anyway)
    prices = std::move(price_vec);
    stock_ticker = std::move(tckr);
    // Using clear guarantees that empty() returns true
    daily_ret.clear();
    mean_return = 0;
    var_return = 0;
    // We want to keep track of what we've computed to avoid redundant calcs
    mean_calced = false;
    var_calced = false;
}

std::vector<double> Stock::dailyReturn() {
    // If the daily returns haven't be calculated yet, we do the calc
    // otherwise we return what we've already stored
    if (daily_ret.empty()) {
        daily_ret.resize(prices.size() - 1);
        // We can simply this calculation into a lambda with two inputs
        // using the stl transform function
        // (pt - ptm1) / ptm1
        std::transform(prices.begin(), prices.end() - 1, prices.begin() + 1,
            daily_ret.begin(), [](double ptm1, double pt)
                       { return (pt - ptm1) / ptm1; } );
    }
    return daily_ret;
}

double Stock::meanReturn() {
    // First we check if we've already calculated the mean
    if (!mean_calced) {
        // If we haven't, we make sure we have the daily returns first
        if (daily_ret.empty())
            dailyReturn();
        // std accumulate adds all the entries for us!
        mean_return = std::accumulate(daily_ret.begin(), daily_ret.end(), 0.0);
        // prices.size() is n
        mean_return /= static_cast<double>(prices.size());
        mean_calced = true;
    }
    return mean_return;
}

double Stock::varReturn() {
    // Have we calculated it already?
    if (!var_calced) {
        // Do we have the mean yet?
        if (!mean_calced)
            meanReturn();
        // Notice that the above will also cascade to dailyReturn if necessary
        // Below we calc the variance sum((r_n - r_mean)^2)/(n - 1)
        for (auto &ret : daily_ret) {
            var_return += pow(ret - mean_return, 2);
        }
        // daily returns is of size n - 1 by definition
        var_return /= static_cast<double>(daily_ret.size());
        var_calced = true;
    }
    return var_return;
}
