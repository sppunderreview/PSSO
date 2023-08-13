def formatTime(s):    
    h = int(s / 3600)
    m = int((s - (h*3600))/ 60)
    s = round(s % 60)
    if h > 0:    
        return str(h)+"h"+str(m)+"m"
    if m > 0:
        return str(m)+"m"+str(s)+"s"
    return str(s)+"s"
	



simCG =   202899.15104198456  + 292313.92229390144
simCFG =  200155.8525595665   + 0

print(formatTime(simCG))
print(formatTime(simCFG))

print(formatTime(292313.92229390144))

# 137h33m (81h11m)
# 55h35m

# / SC
# 0.14584638052334167 + 0.21011880692554072 ( 0.21011880692554072 )
# 0.143874464168339
