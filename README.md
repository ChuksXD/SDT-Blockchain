# BlockchainKnapsack - transaction selection mining algorithm using SDT 
Comparing our proposed Size-Density table (SDT) strategy to different weighted knapsack algorithms for transaction selection from the mempool.
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#Setup)

## General info
We introduce a data structure, SDT that outperforms the widely used transaction selection mining algorithms such as heap-based sorting. It improves performance by supporting insertion & deletion in constant time
and more importantly forms a block without the need to sort transactions.

In addition, the transactions selected by the SDT have a total fee that is comparable and in some cases, better than existing solutions. This enables miners to gain both speed and pofit when adopting our strategy.

The algorithms that we use for comaprison are as follows:
### 
