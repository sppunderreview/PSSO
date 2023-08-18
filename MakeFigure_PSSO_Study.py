from Windows.Redaction.PSSO_Study.PSSO_Study_Preprocessing import readPSSOStudyPreprocessing
from Windows.Redaction.PSSO_Study.PSSO_Study_Precision import readPSSOStudyPrecision

from Windows.Redaction.Windows_Preprocessing import readTableWindowsPreprocessing
from Windows.Redaction.Windows_Precision_RQ2 import readWindowsPrecisionRQ2


import numpy as np
import matplotlib.pyplot as plt


preprocessing = readPSSOStudyPreprocessing()
PreproTimes = [(100, readTableWindowsPreprocessing()["PSSO"]["Average"])]
for nEmb in preprocessing:
	number = int(nEmb[5:])
	PreproTimes += [(number, preprocessing[nEmb])]

precision = readPSSOStudyPrecision()
PrecisionScore = [(100, float(readWindowsPrecisionRQ2()["PSSO"]["AVG"]))]
for nEmb in precision:
	number = int(nEmb[5:])
	PrecisionScore += [(number, precision[nEmb])]

X              =  [i for (i,j) in PrecisionScore]
PreproTimes    =  [j for (i,j) in PreproTimes]
PrecisionScore =  [j for (i,j) in PrecisionScore]

plt.style.use("seaborn-paper")

X = [str(x) for x in X]
PrecisionScore = np.array(PrecisionScore)
PreproTimes = np.array(PreproTimes)
    
fig, ax = plt.subplots()
plt.scatter(PreproTimes, PrecisionScore)

for i, txt in enumerate(X):
    ax.annotate(txt, (PreproTimes[i], PrecisionScore[i]), xytext=(PreproTimes[i], PrecisionScore[i]+0.00005) )

ax.set_xlabel('Average Preprocessing Runtime per Program (sec) on the Windows dataset')
ax.set_ylabel('Precision Score on the Windows dataset')

print(X)
print(PrecisionScore)
print(PreproTimes)

plt.show()

"""
['100', '30', '50', '80', '130', '150', '180']
[0.466      0.4639945  0.46573458 0.46567388 0.46640228 0.46628088 0.46751512]
[0.39305151 0.06069202 0.10626905 0.24974706 0.66635269 0.90708304 1.30903364]
"""
