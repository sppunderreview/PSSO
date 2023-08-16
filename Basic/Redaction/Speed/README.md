# Preliminary Evaluation, Method Selection
## Correction Tables 4 and 5
Issue : Each Basic subdataset has six different test fields (e.g., O0O1, O0O2, O0O3, O1O2, O1O3, O2O3).
Since a program is inside three test fields, we perform three clone searches for each program.
In this regard, we had to measure each program's preprocessing three times in total runtimes, but we counted it only once.

Under this correction, the total preprocessing running times of ASCG, ASCFG, PSS, and PSSO have been multiplied by 3. 
Importantly, runtime spent per clone search for PSS and PSSO remains unchanged at 1.41s and 0.27s, respectively because they have been carefully estimated. 

This  correction yield somewhat different  results from those mentioned in the  submitted version for Tables 4 and 5.
For PSS, the total runtime has gone from 26m7s to 1h18m, and for PSSO, from 5m4s to 15m8s. 

This correction does not alter our original findings. Before this correction, PSS, with a total processing time of 26m7s, was identified as being 32 times faster than the slowest method we previously eliminated, LibDB, with a runtime of 16h. Thus, even after adjusting the processing times by a factor of three, PSS, now at 1h18m, remains 10 times faster than the fastest method previously eliminated. Therefore, the overall impact of this correction is limited.
