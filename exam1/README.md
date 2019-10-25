# This the README for the first exam

I chose a procederial appraoch in this exercise since the relative simplicity of the data we're working with makes the data structures in python suitable. Although the code is not as readable as it may be in an object oriented case, it is faster to implement in the limited time available for the exam, and less prone to potential errors in implementation. The `dict()` is much easier to understand quickly than a whole new class.

To improve the program, more potential cases of bad input should be considered (such as invalid choices of `m`, `k`). Further, an object oriented approach does makes sense in this case and could be implemented if given more time. This would be how I improve the program.

Regarding time complexity of taking the lowest grade, it is purely due to the complexity of finding the lowest value in a list. This is in general O(m) runntime in my implementation since I simply use the python `min()` function. Dropping the lowest grade is constant time since I simply subtract it from the sum.

In the first test case, `test_1.txt` we expect to see student 1 on top with the first assignment dropped since it will come to an average of 1.0. We expect to see student 3 in the middle since he does the second best, and last is student 2 who despite being very consistent still just barely gets in last place.

```
jbarnett8@gauss ~ $ python3 gradebook.py test_1.txt test_1_out.txt 2 1
jbarnett8@gauss ~/Drive/School/Stanford/Fall19/CME211/exam1 $ head test_1_out.txt 
1 0 1.000
3 1 0.575
2 0 0.500

```

This is indeed what we see.

In the second test case, we have a tie between the first and second student, so it won't matter which of the two here are first in the sorted scores. They should both drop any assignment. Student 4 should do better than student 3 since even though the exam scores are bad, they are still better than student 3. Student 3 should have the 2nd assignment dropped.

```
jbarnett8@gauss ~ $ python3 gradebook.py test_2.txt test_2_out.txt 2 1
jbarnett8@gauss ~/Drive/School/Stanford/Fall19/CME211/exam1 $ head test_2_out.txt 
2 0 1.000
1 0 1.000
4 0 0.750
3 1 0.575

```