from Basic.Redaction.Precision.Basic_Precision_RQ2 import readBasicPrecisionRQ2
from Basic.Redaction.Robustness.Basic_Robustness_RQ3 import readBasicRobustness_RQ3
from Basic.Redaction.Speed.Basic_Speed_RQ1 import readBasicSpeedRQ1
from Basic.Redaction.Speed.Basic_Speed_Total_RQ1 import readBasicSpeedTotalRQ1


from BinKit.Redaction.Binkit_Precision_RQ2 import readBinkitPrecisionRQ2
from BinKit.Redaction.Binkit_Robustness_RQ3 import readBinkitRobustnessRQ3
from BinKit.Redaction.Binkit_Speed_RQ1 import readBinkitSpeedRQ1


from IoT.Redaction.IoT_Precision_RQ2 import readIoTPrecicionRQ2
from IoT.Redaction.IoT_Speed_RQ1 import readIoTSpeedRQ1

from Windows.Redaction.Windows_Precision_RQ2 import readWindowsPrecisionRQ2
from Windows.Redaction.Windows_Speed_RQ1 import readWindowsSpeedRQ1

from copy import deepcopy
import pandas as pd
import time

def selectColumnAndName(t, column, newname):
	t2 = deepcopy(t)	
	for f in t:
		d = {}
		d[newname] = t[f][column]
		t2[f] = d
	return t2

def fusionTables(a, b, c, d):
	a2 = deepcopy(a)	
	for f in a2:
		a2[f].update(b[f])
		a2[f].update(c[f])
		a2[f].update(d[f])
	return a2

def printTable(t):
	df = pd.DataFrame(t).T
	df.fillna(0, inplace=True)
	print(df)
	print()
	
start = time.time()

print("Loading the Preliminary Evaluation Table ...")
readBasicSpeedTotalRQ1()
print()
print()

print("Loading RQ1 Tables ...")
basicSpeed = readBasicSpeedRQ1()
binkitSpeed = readBinkitSpeedRQ1()
iotSpeed = readIoTSpeedRQ1()
windowsSpeed = readWindowsSpeedRQ1()

print("Table (RQ1) Total runtimes.\nInclude preprocessing time.\nSignificant preprocessing times reported in \"( )\".")
basicSpeedTotal = selectColumnAndName(basicSpeed, "Total", "Basic")
binkitSpeedTotal = selectColumnAndName(binkitSpeed, "Total", "BinKiT")
iotSpeedTotal = selectColumnAndName(iotSpeed, "Total", "IoT")
windowsSpeedTotal = selectColumnAndName(windowsSpeed, "Total", "Windows")

tableSpeedTotal = fusionTables(basicSpeedTotal, binkitSpeedTotal, iotSpeedTotal, windowsSpeedTotal)
printTable(tableSpeedTotal)

print("Table (RQ1) Runtimes per clone search (sec).\nInclude preprocessing time.\nSignificant preprocessing times reported in \"( )\".")
basicSpeedAVG = selectColumnAndName(basicSpeed, "AVG", "Basic")
binkitSpeedAVG = selectColumnAndName(binkitSpeed, "AVG", "BinKiT")
iotSpeedAVG = selectColumnAndName(iotSpeed, "AVG", "IoT")
windowsSpeedAVG = selectColumnAndName(windowsSpeed, "AVG", "Windows")

tableSpeedAVG = fusionTables(basicSpeedAVG, binkitSpeedAVG, iotSpeedAVG, windowsSpeedAVG)
printTable(tableSpeedAVG)


print("Loading the RQ2 Table ...")
basicPrecision = selectColumnAndName(readBasicPrecisionRQ2(), "AVG", "Basic")
binkitPrecision = selectColumnAndName(readBinkitPrecisionRQ2(), "AVG", "BinKiT")
iotPrecision = selectColumnAndName(readIoTPrecicionRQ2(), "AVG", "IoT")
windowsPrecision = selectColumnAndName(readWindowsPrecisionRQ2(), "AVG", "Windows")

print("Table (RQ2) Precision Scores.")
tableSpeedAVG = fusionTables(basicPrecision, binkitPrecision, iotPrecision, windowsPrecision)
printTable(tableSpeedAVG)


print("Loading RQ3 Tables ...")
readBinkitRobustnessRQ3()
print()
print()

readBasicRobustness_RQ3()
print()
print()

elapsed = time.time() - start
print("All Tables generated in", "{0:.2f}".format(elapsed), "s")
