# RQ1: Evaluation of Speed (Windows)
## Correction
Initially, for PSS and ASCG preprocessing, 30 very large target programs out of a total of 49,443 were run with multiple processors. A coefficient was applied to recover a comparable runtime for query preprocessing. We have replaced this estimate with a computation with one processor. The initial estimation was too optimistic, and the larger and heavier programs are particularly slow on PSS, noticeably influencing the average.

Prior to this correction, the mean preprocessing runtime was 13.42 seconds, and the median was 0.12563, with a minimum time of 0.00139 and a maximum time of 10,074 seconds. 
 
Following the correction, the median remained at 0.12563, with the minimum still at 0.00139. However, the maximum time increased to 19,988 seconds, and the mean was 16.95 seconds.

On average, there is an increase of around 3.53 seconds in the preprocessing for PSS and ASCG. Overall, the total runtime required for PSS went up from 215 hours to 263 hours.  The runtime per clone search for PSS increased from 15.64 to 19.17 seconds. 

This is an increase of 26.3% at the preprocessing level and 22.6% for an entire clone search for PSS and ASCG. 

This correction only applies to PSS and not PSSO; it's optimized version that can deal with larger programs. It confirms the need for PSSO, which has a total runtime of only 31 hours and takes an average of 0.39s to preprocess a Windows program.
