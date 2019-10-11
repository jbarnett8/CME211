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
    """Checks and cleans up program arguments, then returns the cleaned args"""

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
        print('User specified threshold is not a positive integer ' +
              'greater than zero')
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
    """Calculates the cosine similarity value between two movies"""
    mean_a = movies_avg[movie_a]
    mean_b = movies_avg[movie_b]
    sum_a = 0
    sum_b = 0
    P_numerator = 0
    for u_id in common_users:
        user = users[u_id]
        a = (user[movie_a] - mean_a)
        b = (user[movie_b] - mean_b)
        P_numerator += a*b
        sum_a += a**2
        sum_b += b**2
    P_denominator = math.sqrt(sum_a*sum_b)
    if math.isclose(P_denominator, 0):
        P = 0
    else:
        P = P_numerator/P_denominator

    if (P > 1.0):
        print("WARNING: P is greater than 1. There is an error in the code.")
        sys.exit()

    return P

def parse_data(data):
    movies = dict()
    movies_avg = dict()
    users = dict()
    for u_id, m_id, rating, time in data:
        if m_id in movies.keys():
            movies[m_id].add(u_id)
            movies_avg[m_id] += int(rating)
        else:
            movies[m_id] = set({u_id})
            movies_avg[m_id] = int(rating)

        if u_id in users.keys():
            users[u_id].update({m_id:rating})
        else:
            users[u_id] = {m_id:rating}

    for movie, u_ids in movies.items():
        movies_avg[movie] /= len(u_ids)

    return movies, movies_avg, users

# Grab clean program agruments
data_file, out_file, threshold = get_program_args()

# Place to parsed data from output
data = []
# Create dict from database of movies
with open(data_file,'r') as f:
    for line in f:
        data.append(tuple((int(s) for s in line.split())))

movies, movies_avg, users = parse_data(data)

Ps = dict()
movie_pairs = set()
movie_list = []
for movie_a, users_a in movies.items():
    movie_list.append(movie_a)
    for movie_b, users_b in movies.items():
        pair_a = (movie_a, movie_b)
        pair_b = (movie_b, movie_a)
        if (pair_a == pair_b):
            continue
        if (pair_a in movie_pairs) or (pair_b in movie_pairs):
            continue
        movie_pairs.add(pair_a)
        movie_pairs.add(pair_b)
        common_users = users_a.intersection(users_b)
        num_users = len(common_users)
        if (num_users >= threshold):
            P = calc_cosine_similarity(common_users, users, movie_a, 
                                       movie_b, movies_avg)
            if movie_a in Ps.keys():
                Ps[movie_a].append((P, movie_b, num_users))
            else:
                Ps[movie_a] = [(P, movie_b, num_users)]

            if movie_b in Ps.keys():
                Ps[movie_b].append((P, movie_a, num_users))
            else:
                Ps[movie_b] = [(P, movie_a, num_users)]
            # call function

movie_list.sort()
with open(out_file,'w') as f:
    for m_id in movie_list:
        if m_id in Ps.keys():
            P, match, num_users = max(Ps[m_id])
            f.write("{} ({}, {}, {})\n".format(m_id, match, P, num_users))
        else:
            f.write('{}\n'.format(m_id))
