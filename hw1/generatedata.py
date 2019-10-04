import random
import sys
import os
import math

def print_help_text(): 
    print('nreads\t\t:\tThe number of separate ' +
           'read strings')
    print('reference_length:\tThe length of ' + 
           'the reference database')
    print('read_length\t:\tThe length of each ' +
           'of the individual read strings')
    print('reference_file\t:\tThe name of the ' +
           'reference file to output.')
    print('reads_file\t:\tThe name of the ' +
           'reads file to output.')

# These are simple sanity checks, not exhaustive
if (len(sys.argv) < 6):
    print('Missing one or more input arguments.\n')
    print_help_text()
    sys.exit()

# This ensures that the first three agruments are positive integers
if any([not s.isdigit() for s in sys.argv[1:3]]):
    print('One or more of the inputs is not a positive integer.')
    print_help_text()
    sys.exit()

# This may not be a necessary check, but we want to make sure we aren't going
# to ovewrite some other file by accident since it will destroy anything
# if any([os.path.isfile(os.getcwd() + '/' + s) for s in sys.argv[4:6]]):
#     print('One or more of the file names already exists.')
#     print_help_text()
#     sys.exit()


# Defining constants given in the assignment document
PERCENT_RAND_REF_LENGTH = 0.75
SINGEL_MATCH_CUTOFF = 0.75
DOUBLE_MATCH_CUTOFF = 0.85


# Setting common variables from command line
num_reads = int(sys.argv[2])
ref_length = int(sys.argv[1])
read_length = int(sys.argv[3])

# This a check to make sure we have a sane selection for the read length.
# In order to have doubly aligned readas, the read length has to stay 
# below a certain threshold
if (ref_length - math.ceil(PERCENT_RAND_REF_LENGTH*ref_length)) <= read_length:
    print('The read length is too large. Make it smaller.')
    print_help_text()
    sys.exit()

print('reference length: {}\nnumber reads: {}\nread length: {}'.format(
       ref_length, num_reads, read_length))

# first we'll make a reference library random values 
# up to PERCENT_RAND_REF_LENGTH of the specified length
bases = ['A', 'T', 'C', 'G']
rand_ref_length = math.floor(PERCENT_RAND_REF_LENGTH*ref_length)
rep_ref_length = ref_length - rand_ref_length
ref_str =  ''.join(bases[random.randint(0,3)] for i in range(rand_ref_length))

# Copy the last bit to fill the last 25%
ref_str = ref_str + ref_str[-rep_ref_length:]

# Write the reference_file string
with open(sys.argv[4],'w') as f:
    f.write(ref_str)

# Next we generate the reads
read_align_count = [0, 0, 0]
reads = []
for i in range(num_reads):
    rand_num = random.random()

    # This is the case for a single alignment: 75% of the time
    if (rand_num < SINGEL_MATCH_CUTOFF):
        read_align_count[1] += 1
        select = random.randint(0,math.floor(0.5*ref_length))
        reads.append(ref_str[select:select+read_length])
        continue
    # two alignments: 10% of the time
    elif (rand_num < DOUBLE_MATCH_CUTOFF):
        read_align_count[2] += 1
        lower = math.ceil(0.75*ref_length)
        upper = ref_length - read_length
        select = random.randint(lower, upper)
        reads.append(ref_str[select:select+read_length])
        continue
    # no alignments: 15% of the time
    else:
        read_align_count[0] += 1
        while True:
            rand_str = ''.join(bases[random.randint(0,3)] for i in \
                               range(read_length))
            # If the rand_string doesn't exist in the reference string, then
            # we are free to add it, otherwise we try again
            if rand_str not in ref_str:
                reads.append(rand_str)
                break

# Write the result to the specified file
with open(sys.argv[5],'w') as f:
    for s in reads:
        f.write('{}\n'.format(s))


for i, v in enumerate(read_align_count):
    print('aligns {}: {}'.format(i, v/num_reads))