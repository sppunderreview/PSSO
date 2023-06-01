# RQ1: Evaluation of Speed (Windows)
## Correction
Initially, for PSS and ASCG preprocessing, 63 very large programs were run with multiple processors.
A coefficient was applied to recover a comparable runtime.
We have replaced this estimate with a computation with one processor.
The estimation was too optimistic, as seen in the graph below.
![Plot of preprocessing runtimes depending on call graph sizes](./Running_Times.png "Plot of preprocessing runtimes depending on call graph sizes")
The green points are our original estimation of running times, while the blue points are actual running times.

On average, there is an increase of four seconds during the preprocessing phase of PSS and ASCG.
We have corrected PSS and ASCG preprocessing runtimes on Windows.

