# Examples

## PSSO on the Basic Dataset (8 minutes)

**Command:**
```bash
conda activate PSS_Base
python3 SetAbsolutePaths.py
cd PSSO/
python3 Preprocess.py 
```

**Output:**
```console
Program lua with O2, # of local CFG: 817, time: 0.15022063255310059 s
```

**Command:**
```bash
python3 RunMakeMD3.py
```
**Output:**
```console
Basic Subdataset BO
Computing similarity indices for Program lua with O2
tqdm bar
```

**Command:**
```bash
python3 RunMakeMD.py 
```
**Output:**
```console
Basic Subdataset UV 
Testfield V2 -> V3
tqdm bar
Testfield V2 <- V3
tqdm bar
Testfield V2 <-> V3
tqdm bar
```

**Command:**
```bash
cd ../
python3 MakeTables.py
```

**Output:**
```console
...
```


## SAFE function embedding on the Coreutils Versions subdataset (8 minutes)

**Command:**
```bash
conda activate PSS_Base
python3 SetAbsolutePaths.py
cd SAFE/makeEmbeds
python3 computesEmbeddings.py
```
**Output:**
```console
...
```

**Command:**
```bash
python3 readEmbeddings.py
```

**Output:**
IMAGE

You can quit the bash terminal to end the python script.

## StringSet on a hundred IoT malwares (5 minutes)

**Command:**
```bash
conda activate PSS_Base
cd IoT/DataGeneration/STRINGSET/
python3 Preprocess.py
```
**Output:**
```console
IoT malware hash 
String literals: {..}
```

**Command:**
```bash
mv STRINGS ../RESTRICT_EMBEDS/complete
cd ../RESTRICT_EMBEDS/
python3 RestrictToOldVersion.py
```
**Output:**
```console
Size before restriction: 200
Size after restriction: 157
```

**Command:**
```bash
mv final/STRINGS ../../XP/
cd ../../XP/
mkdir RS/
python3 RunSmallStringSet.py 
```

**Output:**
```console
...
```

**Command:**
```bash
cd ../Redaction/
python3 IoT_Small.py
```
**Output:**
```console
         AVG       Precision    Total Clone Search (s)
StringSet 0.01s        0.682            2s
```

## PSSO on a small part of the Windows dataset (7 minutes)

**Command:**
```bash
conda activate PSS_Base
cd Windows/PSSO
unzip EMBEDS.zip
mkdir RS/
python3 RunSmallPSSO.py
```
**Output:**
```console
...
```

**Command:**
```bash
cd ../Redaction/
python3 Windows_Small.py
```
**Output:**
```console
         AVG               Precision    Total Clone Search (s)
PSSO    1.57s (0.39s)        0.430            5h27m(5h23m)
```

## MutantX-S  on the clang v7/v4 testfield of the BinKit dataset (20 minutes)

**Command:**
```bash
conda activate PSS_Base
cd BinKiT/Normal/
unzip EMBEDS.zip
cd EMBEDS/
7z x MUTANTX2.7z
cd ../
mkdir RS/
python3 RunSmallMX.py
```
**Output:**
```console
clang 7.0 vs clang 4.0
/ 7520
17:18
clang-7.0/clang-4.0 1 MUTANTX2 1038.6364123 s
```

**Command:**
```bash
python3 ReadSmall.py
rm -r EMBEDS/
```
**Output:**
```console
MutantX-S results only on clang-7.0_VS_clang-4.0 in one direction.
MUTANTX2 clang-7.0_VS_clang-4.0 5931 7520 0.78869 0.1378890

                  AVG               Precision    Total Clone Search (s)
MutantX-S     0.137889s             0.789            17m17s
```
