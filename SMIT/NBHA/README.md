# Mattias Andrée and Sam Hocevar

𝓞(n³) implementation of the Hungarian algorithm, also known as the Hungarian method, Kuhn–Munkres algorithm or Munkres assignment.

The Hungarian algorithm solves the minmum bipartite matching problem in 𝓞(n⁴).

By implementing the priority queue with a van Emde Boas tree the time can be reduced to 𝓞(n³ log log n).

The van Emde Boas tree is possible to use because the elements values are bounded within the priority queue's capacity.

However this implemention achives 𝓞(n³) by not using a priority queue.

Edmonds and Karp, and independently Tomizawa, has also reduced the time complexity to 𝓞(n³), but I do not known how.

# Tristan Benoit

Modified to perform SMIT specific graph edit distance computation. The 𝓞(n³) is lost in the process.
