import sys
import os
import math
import time

def print_help_text(): 
    print('reference_file\t:\tThe name of the ' +
           'reference file to read.')
    print('reads_file\t:\tThe name of the ' +
           'reads file to read.')
    print('align_file\t:\tThe name of the ' +
           'alignment file to output.')

# These are simple sanity checks, not exhaustive
if (len(sys.argv) < 4):
    print('Missing one or more input arguments.\n')
    print_help_text()
    sys.exit()

# This may not be a necessary check, but we want to make sure we aren't going
# to ovewrite some other file by accident since it will destroy anything
if any([not os.path.isfile(os.getcwd() + '/' + s) for s in sys.argv[1:2]]):
    print('One or more of the input files do not exist.')
    print_help_text()
    sys.exit()

# Open file with reference sequence and store in local variable
with open(sys.argv[1],'r') as f:
    reference = f.read().strip()

# Open file with reads, and make each an entry in a list
reads = []
with open(sys.argv[2],'r') as f:
    for line in f:
        reads.append(line.strip())

start = time.time()

# Setting up storage of counts and alignments, where alignments is
# a list of tuples since the length will vary bewteen 1 and 2
read_align_count = [0, 0, 0]
alignment_data = []
for read in reads:
    # First we want to check if the value is present
    # using the 'in' operation is faster than using find
    # so for large data sets it is better to check if it exists
    # first before iterating through the entire reference string
    if read in reference:
        # find the first match
        loc = reference.find(read)
        # See if we get a second match
        loc2 = reference.find(read, loc + 1)
        # Add to the alignment data depending on the match
        if (loc2 is -1):
            read_align_count[1] += 1
            alignment_data.append((loc))
        else:
            read_align_count[2] += 1
            alignment_data.append((loc, loc2))
    else:
        # No match was found
        read_align_count[0] += 1
        alignment_data.append((-1))

stop = time.time()

# We write the alignment data
with open(sys.argv[3],'w') as f:
    for t in alignment_data:
        f.write('{}\n'.format(t))

# Outputing diagnostic information
print('reference length: {}\nnumber reads: {}'.format(len(reference),
                                                      len(reads)))
for i, v in enumerate(read_align_count):
    print('aligns {}: {}'.format(i, v/len(reads)))

print ('elapsed time: {}'.format(stop - start))