from pathlib import Path
from os.path import isfile
import numpy as np
import matplotlib.pyplot as plt
import pickle
import statsmodels.api as sm
from math import log10
from copy import deepcopy

plt.style.use('seaborn')

def formatTime(s):    
    h = int(s / 3600)
    m = int((s - (h*3600))/ 60)
    s = round(s % 60)
    if h > 0:    
        return str(h)+"h"+str(m)+"m"
    if m > 0:
        return str(m)+"m"+str(s)+"s"
    return str(s)+"s"

with open("QB", "rb") as f:
    E = pickle.load(f) # [Q,B,I,QNames]
    Q = E[0]
    B = E[1]

with open("preprocessQPSS", "rb") as f:
	preprocessQPSS = pickle.load(f)

with open("SPECTRUM_PREPROCESSING_PSS_CORRECTED", "rb") as f:
	SPECTRUM_PSSC = pickle.load(f)
    
# Original estimation
# Adjust runnting times:
# because for PSS preprocessing 63 very large programs were run with multiple processors
# , depending on number of nodes, a coefficient is applied to recover a comparable runtime
preprocessQPSS_NC = {}
for idS in preprocessQPSS:
	if preprocessQPSS[idS][1] > 60000:
		preprocessQPSS_NC[idS] = [preprocessQPSS[idS][0] * 6, preprocessQPSS[idS][1]]
	elif preprocessQPSS[idS][1] > 50000:
		preprocessQPSS_NC[idS] = [preprocessQPSS[idS][0] * 3, preprocessQPSS[idS][1]]


# Correct runnting times:
for idS in preprocessQPSS:
	if preprocessQPSS[idS][1] > 50000:
		preprocessQPSS[idS] = [SPECTRUM_PSSC[idS][1], preprocessQPSS[idS][1]]

X = np.array([preprocessQPSS[idS][1] for idS in Q])
Y = np.array([preprocessQPSS[idS][0] for idS in Q])


a, b, c = np.polyfit(X, Y, 2)
labelPoly = str(a)+"n²+"+str(b)+"n+"+str(c)
P = np.poly1d([a,b,c])
XF = np.linspace(min(X), max(X), 1000)
YF = P(XF) 

regression = sm.OLS(Y, [P(x) for x in X]).fit()
print(regression.summary())
labelPoly = "r^2=%.3f" % (regression.rsquared) 


X2 = np.array([preprocessQPSS_NC[idS][1] for idS in Q if idS in preprocessQPSS_NC])
Y2 = np.array([preprocessQPSS_NC[idS][0] for idS in Q if idS in preprocessQPSS_NC])
print(len(X2),len(preprocessQPSS_NC))

plt.plot(XF, YF, color='r', alpha=0.1, label=labelPoly)
plt.scatter(X, Y, color='b', s=1)
plt.scatter(X2, Y2, color='g', s=3, label="estimation")

plt.ylabel('seconds')
plt.xlabel('n')
plt.legend()
plt.show()


# Total PSS Q
print("PSS Q", formatTime(sum ([preprocessQPSS[idS][1] for idS in Q])))

# Total PSS B
print("PSS B", formatTime(sum ([preprocessQPSS[idS][1] for idS in B])))

"""
30 54
PSS Q 20  429h  5m
PSS B 30   52h 55m
"""