#!/usr/bin/python3

# ? ?
# 2021
# ?

import filecmp

filecmp.clear_cache()
 
for i in range(88):
	for j in range(88):
		if i == j:
			continue		
		if filecmp.cmp("samplesS/"+str(i),"samplesS/"+str(j), shallow=False):
			print("EQ ", i, j)

