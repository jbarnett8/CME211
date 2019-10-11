This is my repo for the second homework in CME 211

# Part 1 writeup

When creating this test data, I made sure to have 10 different numbers for the `user_id` but only three unique numbers for the `movie_id` as was requested in the problem statement. I picked numbers ranging from 1 to 999 since this seemed mostly appropriate given the sample data set. In keeping with the format of the actual data set, each number starts on the same column to mainatin consistent formatting. I did not create a reference solution.

# Part 2 writeup

Running with u.data yields:

<pre><font color="#8AE234"><b>jb0@rice15</b></font>:<font color="#729FCF"><b>~/cme211/hw2</b></font>$ python3 similarity.py ml-100k/u.data out.txt 6
Input MovieLens file: ml-100k/u.data
Output file for similarity data: out.txt
Minimum number of common users: 6
Read 100000 lines with total of 1682 movies and 943 users
Computed similarities in 18.58 seconds
</pre>

The output file:

<pre><font color="#8AE234"><b>jb0@rice15</b></font>:<font color="#729FCF"><b>~/cme211/hw2</b></font>$ head -n 10 out.txt 
1 (885, 0.90, 6)
2 (1153, 0.91, 7)
3 (1061, 0.93, 7)
4 (35, 0.80, 6)
5 (1086, 0.89, 6)
6 (1008, 0.94, 8)
7 (968, 1.00, 7)
8 (590, 0.86, 6)
9 (854, 0.90, 6)
10 (932, 0.93, 6)
</pre>
