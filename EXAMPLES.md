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
Reading .json
Program codeblocks with O1 , # of local CFG: 3642 , time: 1.3974053859710693 s
Program ssh with O2 , # of local CFG: 1622 , time: 0.5432868003845215 s
Program perl with O1 , # of local CFG: 2225 , time: 1.4496872425079346 s
Program openssl with O1 , # of local CFG: 3464 , time: 0.674699068069458 s
Program libgeany.so.0.0.0 with O2 , # of local CFG: 7653 , time: 2.8476717472076416 s
Program libgeany.so.0.0.0 with O1 , # of local CFG: 7209 , time: 2.7797937393188477 s
Program codeblocks with O0 , # of local CFG: 4430 , time: 1.8078033924102783 s
Program sort with O0 , # of local CFG: 368 , time: 0.1629476547241211 s
Program cp with O0 , # of local CFG: 391 , time: 0.09430146217346191 s
Program git with O0 , # of local CFG: 4065 , time: 1.414459228515625 s
Program openssl with O3 , # of local CFG: 3496 , time: 0.7026350498199463 s
Program ssh with O1 , # of local CFG: 1589 , time: 0.5069830417633057 s
Program libgeany.so.0.0.0 with O0 , # of local CFG: 14624 , time: 4.75564432144165 s
Program ruby with O1 , # of local CFG: 5700 , time: 2.687840461730957 s
Program cmp with O0 , # of local CFG: 149 , time: 0.1868577003479004 s
Program diff with O0 , # of local CFG: 365 , time: 0.0939018726348877 s
...
```

**Command:**
```bash
python3 RunMakeMD3.py
```
**Output:**
```console
Basic Subdataset BO
Computing similarity indices for Program codeblocks with O1
100%|| 84/84 [00:00<00:00, 11437.53it/s]
Computing similarity indices for Program ssh with O2
100%|███████████████████| 84/84 [00:00<00:00, 16027.00it/s]
Computing similarity indices for Program perl with O1
100%|███████████████████| 84/84 [00:00<00:00, 26028.48it/s]
Computing similarity indices for Program openssl with O1
100%|███████████████████| 84/84 [00:00<00:00, 32367.62it/s]
Computing similarity indices for Program libgeany.so.0.0.0 with O2
100%|████████████████████| 84/84 [00:00<00:00, 3396.85it/s]
Computing similarity indices for Program libgeany.so.0.0.0 with O1
100%|███████████████████| 84/84 [00:00<00:00, 39034.07it/s]
Computing similarity indices for Program codeblocks with O0
100%|███████████████████| 84/84 [00:00<00:00, 39864.40it/s]
Computing similarity indices for Program sort with O0
100%|███████████████████| 84/84 [00:00<00:00, 46382.51it/s]
Computing similarity indices for Program cp with O0
100%|███████████████████| 84/84 [00:00<00:00, 44727.88it/s]
...
```

**Command:**
```bash
python3 RunMakeMD.py 
```
**Output:**
```console
Basic Subdataset BO
Testfield O0 -> O1
100%|███████████████████| 21/21 [00:00<00:00, 44984.87it/s]
Testfield O0 <- O1
100%|| 21/21 [00:00<00:00, 125649.62it/s]
Testfield O0 <-> O1
100%|███████████████████| 42/42 [00:00<00:00, 65341.53it/s]
Basic Subdataset BO
Testfield O0 -> O2
100%|███████████████████| 21/21 [00:00<00:00, 144869.05it/s]
Testfield O0 <- O2
100%|███████████████████| 21/21 [00:00<00:00, 144631.17it/s]
Testfield O0 <-> O2
100%|███████████████████| 42/42 [00:00<00:00, 66076.81it/s]
Basic Subdataset BO
Testfield O0 -> O3
100%|███████████████████| 21/21 [00:00<00:00, 142294.64it/s]
Testfield O0 <- O3
100%|███████████████████| 21/21 [00:00<00:00, 90153.92it/s]
Testfield O0 <-> O3
100%|███████████████████| 42/42 [00:00<00:00, 38521.93it/s]
...
```

**Command:**
```bash
cd ../
python3 MakeTables.py
```

**Output:**
```console
Loading the Preliminary Evaluation Table ...
Table (Preliminary Evaluation) Total runtimes on the Basic dataset
               Total
...
PSSO          14m28s
...

Loading RQ1 Tables ...
Table (RQ1) Total runtimes.
Include preprocessing time.
Significant preprocessing times reported in "( )".
                       Basic   ...
...
PSSO         14m28s (14m24s)   ...
...

Table (RQ1) Runtimes per clone search (sec).
Include preprocessing time.
Significant preprocessing times reported in "( )".
                     Basic   ...
...
PSSO         0.26s (0.26s)   ...
...

Loading the RQ2 Table ...
Table (RQ2) Pecision Scores.
            Basic  ...
...
PSSO         0.38  ...
...

Table (RQ3) Average rank-biserial correlation for H on the Basic dataset.
                              CO              UO              BO         Average
...
PSSO               \textbf{0.12}   \textbf{0.09}  \textbf{-0.02}   \textbf{0.06}
...

...

All Tables generated in 101.98 s
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
Computing Coreutils Versions functions embeddings for each program! (5 minutes)
 100%|████████████████████| 348/348 [04:15<00:00,  1.36it/s]
```

**Command:**
```bash
python3 readEmbeddings.py
```

**Output:**
# of unique function names: 5083
```console
Function: .init_proc
Inside 348 programs of Coreutils Versions
...
```

You can quit the bash terminal to end the visualization script.

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