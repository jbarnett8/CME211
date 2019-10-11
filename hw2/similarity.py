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
    """
    Checks and cleans up program arguments, then returns the cleaned args

    Returns:
        data_file (string): Name of the file containing movie review data
        out_file (string): Name of the file to write the similarity data
        threshold (int): The minimum number of common reviewers to give a score
    """

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
    """
    Calculates the cosine similarity value between two movies m_id_a & m_id_b

    Parameters:
        common_users (set): Set of common user_id values that reviewed both
                            movie_a and movie_b
        users (dict): Dictionary containing each user as the key and gives
                            another dictionary of containing m_id:score
        movie_a (int): The m_id key value for the first movie
        movie_b (int): The m_id key value for the second movie
        movies_avg (dict): A dictionary containing the averages for each m_id

    Returns:
        float: a float representing the cosine similarity value between a & b
    """
    mean_a = movies_avg[movie_a]
    mean_b = movies_avg[movie_b]
    sum_a = 0
    sum_b = 0
    P_numerator = 0
    for u_id in common_users:
        # Calculating the individual components of the value P
        user = users[u_id]
        a = (user[movie_a] - mean_a)
        b = (user[movie_b] - mean_b)
        P_numerator += a*b
        sum_a += a**2
        sum_b += b**2
    # Finding the denominator of P
    P_denominator = math.sqrt(sum_a*sum_b)

    # Handling the case where the denominator is very nearly or exactly 0
    if math.isclose(P_denominator, 0):
        P = 0
    else:
        P = P_numerator/P_denominator

    # A simple sanity check that should always be true, otherwise somethings off
    if (P > 1.0):
        print("WARNING: P is greater than 1. There is an error in the code.")
        sys.exit()

    return P

def parse_data(data):
    """
    Organize info from data into easy to index dict containers

    Parameters:
        data (list): list of tuples containing info on each review

    Returns:
        dict: A dictionary matching m_id to set of user ids
        dict: A dictionary matching m_id to its average rating
        dict: A dictionary matching u_id to dict of m_id to rating
    """

    # Declare our individual dictionaries for storage
    movies = dict()
    movies_avg = dict()
    users = dict()
    for u_id, m_id, rating, time in data:

        # If the key is present, we append to the set of users who rated,
        # otherwise, we initialize the set. Similarly, we add the rating
        if m_id in movies.keys():
            movies[m_id].add(u_id)
            movies_avg[m_id] += int(rating)
        else:
            movies[m_id] = set({u_id})
            movies_avg[m_id] = int(rating)

        # Same as above, but we add dictionary entries matching the movie
        # id to the rating from the user
        if u_id in users.keys():
            users[u_id].update({m_id:rating})
        else:
            users[u_id] = {m_id:rating}

    # We need to find the average rating, so divide by num ratings
    for movie, u_ids in movies.items():
        movies_avg[movie] /= len(u_ids)

    return movies, movies_avg, users

################################################################################
## BEGINNING PROGRAM ###########################################################
################################################################################

# Grab clean program agruments
data_file, out_file, threshold = get_program_args()

# Place to parsed data from output
data = []
# Create dict from database of movies
with open(data_file,'r') as f:
    for line in f:
        data.append(tuple((int(s) for s in line.split())))

movies, movies_avg, users = parse_data(data)

# Make dictionary to hold P values, and set to hold unique movie pairs
Ps = dict()
movie_pairs = set()
movie_list = []

# The double for-loop gives us every combination of movie a and movie b
# however, the values between a and b are symmetric, so we do some work
# to avoid double calculating values unnecessarily
for movie_a, users_a in movies.items():
    # We don't have a list of m_id values, so we make it here since the list
    # will be easier to sort, and can serve as source of key values later
    movie_list.append(movie_a)
    for movie_b, users_b in movies.items():
        # The pair a and b is the same as b and a since the order is irrelevant
        pair_a = (movie_a, movie_b)
        pair_b = (movie_b, movie_a)

        # We don't care about the diagonal terms since it provides no info
        if (pair_a == pair_b):
            continue

        # If we've already calculated a particular pair, we can move on
        if (pair_a in movie_pairs) or (pair_b in movie_pairs):
            continue

        # We add both pairs to avoid redundant calculations later
        movie_pairs.add(pair_a)
        movie_pairs.add(pair_b)

        # The intersection of the two sets tells us the common reviewers
        common_users = users_a.intersection(users_b)
        num_users = len(common_users)

        # If it meets the threshold, we calculate the proper output
        if (num_users >= threshold):
            P = calc_cosine_similarity(common_users, users, movie_a, 
                                       movie_b, movies_avg)

            # As we've done before, we append a tuple if key is present,
            # otherwise we initalize the list of tuples
            if movie_a in Ps.keys():
                Ps[movie_a].append((P, movie_b, num_users))
            else:
                Ps[movie_a] = [(P, movie_b, num_users)]

            if movie_b in Ps.keys():
                Ps[movie_b].append((P, movie_a, num_users))
            else:
                Ps[movie_b] = [(P, movie_a, num_users)]
            # call function

# We sort the movies, then print the values given by the movie key from Ps
movie_list.sort()
with open(out_file,'w') as f:
    for m_id in movie_list:
        if m_id in Ps.keys():
            P, match, num_users = max(Ps[m_id])
            f.write("{} ({}, {}, {})\n".format(m_id, match, P, num_users))
        else:
            f.write('{}\n'.format(m_id))
