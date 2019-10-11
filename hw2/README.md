This is my repo for the second homework in CME 211

# Part 1 writeup

When creating this test data, I made sure to have 10 different numbers for the `user_id` but only three unique numbers for the `movie_id` as was requested in the problem statement. I picked numbers ranging from 1 to 999 since this seemed mostly appropriate given the sample data set. In keeping with the format of the actual data set, each number starts on the same column to maintain consistent formatting. Further, we notice that users appear multiple times reviewing different movies, but only one review per movie per user. I created a reference solution using a simple spreadsheet since the data-set was so small, and implementing the cosine similarity is simply done with such a small set.

# Part 2 writeup

Running with `u.data` yields:

<pre><font color="#8AE234"><b>jb0@rice08</b></font>:<font color="#729FCF"><b>~/cme211/hw2</b></font>$ python3 similarity.py ml-100k/u.data out.txt
Input MovieLens file: ml-100k/u.data
Output file for similarity data: out.txt
Minimum number of common users: 5
Read 100000 lines with total of 1682 movies and 943 users
Computed similarities in 18.957 seconds
</pre>

The output file:

<pre><font color="#8AE234"><b>jb0@rice08</b></font>:<font color="#729FCF"><b>~/cme211/hw2</b></font>$ head -n 10 out.txt 
	1 (  918, 0.91,   5)
	2 ( 1056, 1.00,   5)
	3 ( 1081, 0.98,   5)
	4 (   35, 0.80,   6)
	5 (  976, 0.93,   5)
	6 (  279, 0.96,   5)
	7 (  968, 1.00,   7)
	8 (  590, 0.86,   6)
	9 (  113, 0.96,   5)
   10 ( 1202, 0.97,   5)
</pre>

My program works by first parsing the data into an easy to use list of tuples, which I can feed into a for loop by unpacking. Using the unpacked values, I can make a few dictionaries that contain the data I need. The dictionary indexed with movie ids `m_id` named `movies` contains a `set()` of each of the reviewer ids `u_id` such that I can use `intersection()` to easily find the common users between movies as fast as possible. Once I have the set of `common_users`, I can index the previous dictionary of users which contains an additional dictionary indexed with movie ids and returns the reviewer's rating. From this data, it is easy to compute the necessary values to calculate the cosine similarity value between two movies.