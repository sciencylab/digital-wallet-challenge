# Digital wallet challenge

This is a past [Insight data engineering programming challenge](https://github.com/InsightDataScience/digital-wallet), from November 2016 I think.

## Table of content
1. How to install and get it up and running
2. Program summary statistics
3. Introduction
4. Architecture
5. Datasets
6. Engineering challenges
7. Trade-offs
8. Tests


## How to install and get it up and running
To run this repo, it is required that you have
- python3

installed. No external library is used or required.

However, you will need to download the input files. The **batch_payment.txt** file can be downloaded from https://www.dropbox.com/s/y6fige3w1ohksbd/batch_payment.csv?dl=0 and the **stream_payment.txt** file can be downloaded from https://www.dropbox.com/s/vrn4pjlypwa2ki9/stream_payment.csv?dl=0. You may need to rename them to **batch_payment.txt** and **stream_payment.txt**, respectively.

To run using the top-level run.sh script, it will be
assumed you have some sort of a linux environment. In which case, type in
```bash
chmod +x run.sh
./run.sh
```

This program takes approximately 8 minutes to run to completion with my Intel i5 2.2GHz CPU.

Inside the script is a single command:
```bash
python3 ./src/antifraud.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt 1
```
The last parameter is an integer. Please set it to
- 0, if you prefer nothing be printed to the screen,
- 1, if you prefer to know what the program is doing, and
- 2, if you further want to see the ill-formed lines in the input files that the program is programmed to ignore.

### Program summary statistics
Running the library and the functions using a 2.20 GHz CPU, I was able to make the following estimates.

Approximate time needed to read and parse the batch_payment file into a list of ordered pairs: 6~7 seconds.

Approximate time needed to build the transaction network from the list of transaction pairs: ~ 3 seconds.

Average time it takes to ascertain the degree of separation of two nodes:

|degree separated|verification time|
|---|---|
|2  |~10 micro seconds |
|4  |~50 micro seconds |

Time needed to process the entire stream file according to feature:

|feature|time taken|
|---|---|
|1 |~7 seconds |
|2   | ~9 seconds|
|3   | ~7 minutes |



<hr/>

## Introduction
The **Digital Wallet Coding Challenge** by Insights is a simulation into processing payment transactions.

The user starts with a pre-existing network of transaction data (given in batch_payment.txt) and uses it to help prevent fraudulent transactions. It is done by flagging transactions by parties (sender and receiver) who are separated by at least a threshold degree of separation in the transaction network.

In Feature 1, the threshold is 2, meaning that transactions between parties who have not transacted with each other before are flagged. Hence, only transactions of degrees 0 and 1 are allowed without being flagged. In Feature 2, the threshold is 3 and so degrees of separation <= 2 are allowed without being flagged. In Feature 3, the threshold is 4 degrees of separation.

Further, as the transaction data are being streamed, each new transaction is assumed to be valid even if flagged. Meaning, even if receiver A and sender B are flagged, future transactions between the two will proceed smoothly since their new degree of separation is 1.

The program takes in 2 inputs (the batch and stream payment files) and outputs 3 output files, one for each feature. Each line of an output file will contain a single word: "unverified" if flagged by the feature; "trusted" if otherwise.

## Architecture

This problem is fairly straight-forward. The transaction network is modeled as an undirected graph and represented in the background as an "adjacency list."

The initial graph is built using data from a given batch_payment.txt file. And subsequent data is provided by stream_payment.txt. Each new transaction is added the graph immediately after deciding whether or not to flag it.

## Dataset

- [batch_payment.txt](https://www.dropbox.com/s/y6fige3w1ohksbd/batch_payment.csv?dl=0)
- [stream_payment.txt](https://www.dropbox.com/s/vrn4pjlypwa2ki9/stream_payment.csv?dl=0)

## Engineering challenges

The main engineering challenges are simply to be able to determine whether two nodes are within a certain degree of separation apart, and to be able to update the network fast enough.

While there were other problems, those largely pertained to the idiosyncrasies of the programming language I was using, namely python.

## Trade-offs

The three main approaches I considered for determining the degree of separation are
1. a straight-forward breadth-first search (BFS),
2. building graphs of higher degree of separations, and
3. using a bi-directional BFS.

Their trade-offs are as follows.
1. This is straight-forward and its graph is simple to update, but becomes far too slow once the threshold degree is increased to beyond 2. And so, this became unfeasible when implementing Feature 3.
2. This is the fastest of the 3 options and the graph of the higher order separations is not hard to build either. However, the higher-order graphs become increasingly complicated and expensive to update. If the graph did not need to be updated every time a new transaction appeared, this could actually be a feasible approach.
3. The bi-directional BFS approach is actually only slightly more complicated than approach 1, the uni-directional BFS approach, but is much faster for large networks. Where as the cost of BFS (approach 1) increases as k^n, where n is the degree of separation and k is some constant, the cost of the bi-directional BFS increases k^{n/2}. While still costly for large n, this proved to be manageable for the given datasets.


## Tests

Since when errors occur, I find it helpful to be able to interact with the program to probe the problem, the tests have not yet been automated. Instead they are contained in the jupyter notebooks:
- test-graph_creation.ipynb
- test-deep_copy.ipynb
- test-distance_functions.ipynb
- test-features.ipynb

I expect to finish automating the tests in the style Insight wants by the end of May 14th, 2019.
