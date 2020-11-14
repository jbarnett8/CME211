#include <vector>
#include <string>


class Stock {
    private:

        /* private member variables */

    public:

        /* public member variables */

        //constructor
        Stock( std::vector<double> price_vec, std::string tckr);
         
        //calculate daily return
        std::vector<double> dailyReturn( /*add args if neccecary*/ );

        //calculate mean return 
        double meanReturn( /*add args if neccecary*/ );
        
        //calcualte return variance
        double varReturn( /*add args if neccecary*/ );
        
        /* add additional methods as needed */        
};
