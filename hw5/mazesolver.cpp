#include <iostream>
#include <fstream>
#include <string>
using namespace std;

void print_help();
void get_nums_from_line(const string &line, int &a, int &b);
const int ARRAY_SIZE = 20;
enum Direction {UP, DOWN, LEFT, RIGHT};


int main(int argc, char** argv) {

    // Simple check that we have the right # of arguments
	if (argc != 3) {
	    cout << "Incorrect number of program arguments." << endl;
        print_help();
	    exit(1);
	}

    // Allocate our static array containing the maze data
    int M[ARRAY_SIZE][ARRAY_SIZE];
    for (auto &v : M)
        for (auto &vv : v)
            vv = 0;

    // Declaring storage for reading/writing files, then opening
	string line;
	ifstream maze(argv[1]);
	ofstream solution(argv[2]);
	int rows, cols;

	// Make sure we actually opened the files
	if (maze.is_open()) {

	    // Get the first line, then grab the values
		getline(maze, line);
		get_nums_from_line(line, rows, cols);

		// Checking size of the maze
		cout << "rows: " << rows << ", cols: " << cols << endl;
		if ((rows > ARRAY_SIZE) || (cols > ARRAY_SIZE)) {
		    cout << "One or more maze dimension is greater than " << ARRAY_SIZE << "." << endl;
		    print_help();
		    exit(1);
		}

		// Populate the M array with data from maze data file
		while ( getline(maze, line) ) {
		    int row, col;
		    get_nums_from_line(line, row, col);
		    M[row][col] = 1;
		}

		maze.close();

	} else {
		cout << "couldn't open maze file" << endl;
		print_help();
		exit(1);
	}

    for (auto &v : M) {
        cout << endl;
        for (auto &vv : v) {
            cout << vv << ", ";
        }
    }
    cout << endl;

	// Check if solution file is open and write in place
	if (solution.is_open()) {
	    int cur_pos_r = 0, cur_pos_c = 0, sol_r = rows - 1, sol_c = 0;
	    while (M[cur_pos_r][cur_pos_c] == 1) {
	        cur_pos_c++;
	    }
        while (M[sol_r][sol_c] == 1) {
            sol_c++;
        }
	    cout << cur_pos_r << ", " << cur_pos_c << endl;
        cur_pos_c++;
	    // We define a heading with two values:

        

		solution.close();
	} else {
		cout << "couldn't open solution file" << endl;
		print_help();
		exit(1);
	}
}

void print_help() {
    cout << "Mazesolver solves a maze using the right-wall following rule" << endl;
    cout << "maze file: \t name of the file containing maze data" << endl;
    cout << "solution file: \t name of the file to write solution to" << endl;
}

void get_nums_from_line(const string &line, int &a, int &b) {
    auto loc = line.find(' ');
    a = atoi(line.substr(0, loc).c_str());
    b = atoi(line.substr(loc + 1).c_str());
}