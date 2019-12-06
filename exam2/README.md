# Exam 2 Writeup

## Question 1
All of the member variables are private, and they include two `std::vector<double>` members that store the list of prices and daily returns, a `std::string` that stores the ticker name, two floating point `double` terms holding the mean return and variance, and finally two `bool` members that determine whether or not a calculation has already been performed to avoid redunancy.

The reason these members are all private is to support encapsulation. The only way users can access these values is through function calls which is a part of good OOP design and also guarantees that users will not accidentally modify the values which are used by the public methods.

## Question 2
Both `dailyReturn()` and `meanReturn()` accept no arguments. This is because all the data required to calculate these values is already present within the class itself, which saves the user the headache of having to pass (for instance) the list of prices. As the designer of the class, we can know when we've already calculated something necessary to calculate something else (like the list of daily returns which is required to calculate its average).

## Question 3
To minimize repetative calls I include two `bool` values to tell the class whether or not its already calculated the mean and variance as well as the `empty()` function used on `vector` classes. The list of daily returns is initally empty since we call `clear()` from the beginning, and the `bool` values are set such that the first time a calculation is requested, it will do the calculation, but than flip to avoid this. This is important since the public functions call each other which the user can still call themselves, so these help avoid too much wasted time.

## Question 4
The keyword `new` does not appear in my program as standard library objects (like `std::vector<double>`) are far more appropriate and robust for this application. These objects will handle the memory for me and gargabe collect when going out of scope.

## Question 5
The part of my program I am most proud of is the relative efficiency and ease of use for the end user. For instance, if the user wanted to simply calculate the variance of the daily returns, all he or she must do is call `varReturn()` which will automatically cascade through all of the required prerequisite calculations automatically to find this value. This is instead of having to call all of the other public functions the class has already. Better still, if any of the other functions are called subsequently, the stored values from earlier are simply returned as opposed to re-calculating.