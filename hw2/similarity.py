import math
import os
import sys

def print_help_text():
    """Prints program help text"""

    print('INPUT ARGUMENTS')
    print('data file\t:\tSource of move review information')
    print('output file\t:\tOutput file name')
    print('threshold\t:\t(OPTIONAL) positive integer to sepcify the ' + 
          'minimum number of common users to compute a score ')

def get_program_args():
    """Checks and cleans up program arguments, then returns"""

    DEFAULT_THRESHOLD = 5
    # These are simple sanity checks, not exhaustive
    if (len(sys.argv) < 3):
        print('Missing one or more input arguments.\n')
        print_help_text()
        sys.exit()
    if (len(sys.argv) > 4):
        print('Too many input arguments.\n')
        print_help_text()
        sys.exit()

    # Store values, set defaults
    data_file = sys.argv[1]
    out_file  = sys.argv[2]
    threshold = DEFAULT_THRESHOLD

    # Check if user defined a threshold, and make sure it's a positive int
    if (len(sys.argv) == 4 and not sys.argv[3].isdigit()):
        print('User specified threshold is not a positive integer')
        print_help_text()
        sys.exit()
    elif (len(sys.argv) == 4):
        threshold = int(sys.argv[3])

    # We want to make sure that the source file actually exists
    if not os.path.isfile(os.getcwd() + '/' + data_file):
        print('The source file does not exist.')
        print_help_text()
        sys.exit()

    return (data_file, out_file, threshold)

def calc_cosine_similarity(common_users, users, movie_a, movie_b, movies_avg):
    print('test')

# Grab clean program agruments
data_file, out_file, threshold = get_program_args()

# Place to parsed data from output
data = []
# Create dict from database of movies
with open(data_file,'r') as f:
    for line in f:
        data.append(tuple((int(s) for s in line.split())))

# [print(s) for s in data]
# [print((u_id, m_id, rating, time)) for u_id, m_id, rating, time in data]

movies = dict()
movies_avg = dict()
users = dict()
for u_id, m_id, rating, time in data:
    if m_id in movies.keys():
        movies[m_id].add(u_id)
        movies_avg[m_id] += rating
    else:
        movies[m_id] = set({u_id})
        movies_avg[m_id] = rating

    if u_id in users.keys():
        users[u_id].update({m_id:rating})
    else:
        users[u_id] = {m_id:rating}


P_ab = dict()
movie_pairs = set()
for movie_a in movies.items():
    for movie_b in movies.items():
        pair_a = (movie_a[0], movie_b[0])
        pair_b = (movie_b[0], movie_a[0])
        if (pair_a == pair_b):
            continue
        if (pair_a in movie_pairs) or (pair_b in movie_pairs):
            continue
        movie_pairs.add(pair_a)
        movie_pairs.add(pair_b)
        common_users = movie_a[1].intersection(movie_b[1])
        if (len(common_users) >= 5):
            print('call function')
            # call function

