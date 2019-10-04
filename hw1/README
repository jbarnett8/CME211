This is the repo for my first homeowkr assignment for CME 211

# Part 2 Writeup

Outputs:
```
jbarnett@newton:~/Drive/School/Stanford/Fall19/CME211/hw1$ python3 generatedata.py 1000 600 50 "ref_1.txt" "reads_1.txt"
reference length: 1000
number reads: 600
read length: 50
aligns 0: 0.14
aligns 1: 0.745
aligns 2: 0.115
jbarnett@newton:~/Drive/School/Stanford/Fall19/CME211/hw1$ python3 generatedata.py 10000 6000 50 "ref_2.txt" "reads_2.txt"
reference length: 10000
number reads: 6000
read length: 50
aligns 0: 0.15166666666666667
aligns 1: 0.7421666666666666
aligns 2: 0.10616666666666667
jbarnett@newton:~/Drive/School/Stanford/Fall19/CME211/hw1$ python3 generatedata.py 100000 60000 50 "ref_3.txt" "reads_3.txt"
reference length: 100000
number reads: 60000
read length: 50
aligns 0: 0.14911666666666668
aligns 1: 0.7516833333333334
aligns 2: 0.0992

```


When designing the handwritten test data, I simply came up with an interesting pattern (which is not relevant to the problem) up to a certain length, then made a duplicate of a snippet that could count as a double alignment to fill it out to the specified length of the reference sequence. When selecting the reads, I just followed the instructions and picked out available alignments. The only tricky part was the sequence that is double counted, but this was already accounted for in the construction of the reference sequence. If my program were to work on my test data, it does not by any means suggest that my program will pass all other datasets. There are multiple edge cases available especially as they relate to the size of the reads and the reference sequence itself.

We should not expect exactly the distrubtion descibed in the program description on an a single execution basis. However, if we increase the number of reads to be sufficiently large, we should see it assympotitcally approach our perscribed distribution. We could also see effects for when the size of the reads approaches the size of the reference sequence, in which case it may not be possible to create a doublely aligned read.

I spent roughly 3 hours working on the code.

# Part 3 Writup

Output:
```
jbarnett@newton:~/Drive/School/Stanford/Fall19/CME211/hw1$ python3 processdata.py ref_1.txt reads_1.txt align_1.txt
reference length: 1000
number reads: 600
aligns 0: 0.14
aligns 1: 0.74
aligns 2: 0.12
elapsed time: 0.002106189727783203
jbarnett@newton:~/Drive/School/Stanford/Fall19/CME211/hw1$ python3 processdata.py ref_2.txt reads_2.txt align_2.txt
reference length: 10000
number reads: 6000
aligns 0: 0.15166666666666667
aligns 1: 0.7416666666666667
aligns 2: 0.10666666666666667
elapsed time: 0.1603388786315918
jbarnett@newton:~/Drive/School/Stanford/Fall19/CME211/hw1$ python3 processdata.py ref_3.txt reads_3.txt align_3.txt
reference length: 100000
number reads: 60000
aligns 0: 0.14911666666666668
aligns 1: 0.7516833333333334
aligns 2: 0.0992
elapsed time: 15.499485492706299
```

The distribution for the zero alignment matches exactly up to the reported precision. This is not suprising since we intentionally required that reads with zero alignment cannot occur in the reference (as we threw out any randomly generated string that did occur). Interestingly, the one and two alignment cases are close but not exactly the same. Thinking logically, it should be possible that a string created to have a single alignment may coincidentally have another alignment that was not intended simply due to the random string generation. We should expect this number to be low, and that the two aignment cases would be slightly higher than the numbers we see from the generation program. This is indeed what we see (except for the last test case).

Extrpolating to the human genome, we see a growth in time proportional to `a * m * n` where `a` is a constant, `m` is the number of reads, and `n` is the length of the reference string. In this case, `a` is roughly 2.6E-9. The genome size for a human is given as roughly `3E9` with 30x coverage. This means we would have `1.8E9` reads. Using the constant from before, this would take roughly 450 years to calculate. This is not feasible.

I spent roughly an hour on this code.