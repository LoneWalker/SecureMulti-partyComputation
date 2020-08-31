# Secure Multi-party Computation
This project implements Threshold based Secure Dot Product Protocol using FastGC. This fascilitates two user Alice and Bob to securely compute dot product of two vectors without revealing one's vector to another. Both vectors mush have the same dymension.

Since GCParser does not have multiplication function, we have to implement it ourselves. We used a python script to generate corresponding circuit file for multiplication. In order to determine dot product we just needed to repeat the multiplication vector size number of times and add all the results of individual multiplication. Then we compare the result with the threshold value.

