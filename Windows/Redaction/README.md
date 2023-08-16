# RQ1: Evaluation of Speed (Windows)
## Correction Tables 5 and 6

**Issue:**
We realized that the reported results  for PSS and ASCG preprocessings were incorrect for 30 very large target programs out of a total of 49,443. It turns out that the PSS preprocessing step is really slow on these examples, noticeably influencing the average -- and demonstrating even more the need for our PSSO optimization. 


Prior to this correction, PSS mean preprocessing runtime was 13.42 seconds, and the median was 0.12563, with a minimum runtime of 0.00139 and a maximum runtime of 10,074 seconds. 
 
Following the correction, the median remains at 0.12563, with the minimum still at 0.00139. However, the maximum runtime increases to 19,988 seconds, and the mean is now 16.95 seconds.

On average, there is an increase of around 3.5 seconds in the preprocessing time for PSS and ASCG for Table 6. The runtime per clone search for PSS increased from 15.64 to 19.17 seconds. Overall, the total runtime for Table 5 required for PSS went up from 215 hours to 263 hours.  

This is an increase of 26.3% at the preprocessing level and 22.6% for an entire clone search for PSS and ASCG. 

This correction only applies to PSS and not PSSO, the optimized version that can deal with larger programs. It confirms the need for PSSO, which has a total runtime of only 31 hours and takes an average of 0.39s to preprocess a Windows program.
