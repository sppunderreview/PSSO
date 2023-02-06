#!/usr/bin/python3

# ? ?
# 2021
# ?

import filecmp

filecmp.clear_cache()
 
for i in range(84):
	for j in range(84):
		if i == j:
			continue		
		if filecmp.cmp("samples/"+str(i),"samples/"+str(j), shallow=False):
			print("EQ ", i, j)

