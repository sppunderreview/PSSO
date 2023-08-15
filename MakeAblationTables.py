from Basic.Redaction.Speed.Ablation.Basic_Ablation_Speed import readBasicAblationSpeed
from Basic.Redaction.Precision.Basic_Ablation_Precision import readBasicAblationPrecision

from BinKit.Redaction.Ablation.Binkit_Ablation_Speed import readBinkitAblationSpeed
from BinKit.Redaction.Ablation.Binkit_Ablation_Precision import readBinkitAblationPrecision
from BinKit.Redaction.Binkit_Precision_RQ2 import readBinkitPrecisionRQ2
from BinKit.Redaction.Binkit_Speed_RQ1 import readBinkitSpeedRQ1

from IoT.Redaction.IoT_Ablation_Precision import readIoTAblationPrecision 
from IoT.Redaction.IoT_Ablation_Speed import readIoTAblationSpeed

from Windows.Redaction.Windows_Ablation_Precision import readWindowsAblationPrecision
from Windows.Redaction.Windows_Ablation_Speed import readWindowsAblationSpeed

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

print("Table 4: PSS Components Precision Scores")
basicPrecision = selectColumnAndName(readBasicAblationPrecision(), "AVG", "Basic")
binkitPrecision = selectColumnAndName(readBinkitAblationPrecision(), "AVG", "BinKiT")
binkitPrecision["PSS"] = selectColumnAndName(readBinkitPrecisionRQ2(), "AVG", "BinKiT")["PSS"]
iotPrecision = selectColumnAndName(readIoTAblationPrecision(), "AVG", "IoT")
windowsPrecision = selectColumnAndName(readWindowsAblationPrecision(), "AVG", "Windows")

tablePrecisionAVG = fusionTables(basicPrecision, binkitPrecision, iotPrecision, windowsPrecision)
printTable(tablePrecisionAVG)

print("Table 5: PSS Components Runtimes per clone search (sec)")
basicSpeed = selectColumnAndName(readBasicAblationSpeed(), "AVG", "Basic")
binkitSpeed = selectColumnAndName(readBinkitAblationSpeed(), "AVG", "BinKiT")
binkitSpeed["PSS"] = selectColumnAndName(readBinkitSpeedRQ1(), "AVG", "BinKiT")["PSS"]
iotSpeed = selectColumnAndName(readIoTAblationSpeed(), "AVG", "IoT")
windowsSpeed = selectColumnAndName(readWindowsAblationSpeed(), "AVG", "Windows")

tableSpeedAVG = fusionTables(basicSpeed, binkitSpeed, iotSpeed, windowsSpeed)
printTable(tableSpeedAVG)

elapsed = time.time() - start
print("All Tables generated in", "{0:.2f}".format(elapsed), "s")
