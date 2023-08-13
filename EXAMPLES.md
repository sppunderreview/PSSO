# Examples

## Basic Dataset: PSSO (8 minutes)
Replicate our method Program Spectral Similarity Optimized (PSSO) on the Basic dataset.

This process will encompass everything from preprocessing to the generation of tables, including the computation of similarity indices.

### Preprocessing
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

### Similarity Indices Computation
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

### Clone Searches on all Test Fields
**Command:**
```bash
python3 RunMakeMD.py 
```
**Output:**
```console
Basic Subdataset BO
Test Field O0 -> O1
100%|███████████████████| 21/21 [00:00<00:00, 44984.87it/s]
Test Field O0 <- O1
100%|| 21/21 [00:00<00:00, 125649.62it/s]
Test Field O0 <-> O1
100%|███████████████████| 42/42 [00:00<00:00, 65341.53it/s]
Basic Subdataset BO
Test Field O0 -> O2
100%|███████████████████| 21/21 [00:00<00:00, 144869.05it/s]
Test Field O0 <- O2
100%|███████████████████| 21/21 [00:00<00:00, 144631.17it/s]
Test Field O0 <-> O2
100%|███████████████████| 42/42 [00:00<00:00, 66076.81it/s]
Basic Subdataset BO
Test Field O0 -> O3
100%|███████████████████| 21/21 [00:00<00:00, 142294.64it/s]
Test Field O0 <- O3
100%|███████████████████| 21/21 [00:00<00:00, 90153.92it/s]
Test Field O0 <-> O3
100%|███████████████████| 42/42 [00:00<00:00, 38521.93it/s]
...
```
### Tables Generation
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
Table (RQ2) Precision Scores.
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


## SAFE Function Embedding on the Coreutils Versions Subdataset (8 minutes)
Demonstrate the use of SAFE Function Embedding.

Due to the time-intense process of SAFE clone searches (655 hours),  only part of SAFE preprocessing is shown in this example.

It replicates SAFE on the subdataset Coreutils Versions of the Basic dataset and allows the user to visualize function embeddings.

### Function Embeddings Computation
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

### Function Embeddings Visualization
**Command:**
```bash
python3 readEmbeddings.py
```

**Output:**
```console
\# of unique function names: 5083
Function: .init_proc
Inside 348 programs of Coreutils Versions
...
```

![Image of SAFE function embeddings for .init_proc from Coreutils Versions](./SAFE/makeEmbeds/init_proc_CV.png "Image of SAFE function embeddings for .init_proc from Coreutils Versions")

You can quit the bash terminal to end the visualization script.

## StringSet on a hundred IoT Malware (5 minutes)

Replicate the method StringSet on 157 IoT Malware samples.

This example goes from the preprocessing that extracts string literals to the generation of tables.

It includes clone searches and the selection of samples.

### Preprocessing
**Command:**
```bash
conda activate PSS_Base
cd IoT/DataGeneration/STRINGSET/
python3 Preprocess.py
```
**Output:**
```console
IoT malware hash: 2a87e1c78db87d283f79adff2d5e4c29e085dd7e931fbb91326af22e8ef7ff0d.elf
String literals: ['n+A\t', 'ff/F/', ... , 'h!d!`!\\!X!T!P!L!H!x!t!p!l!4!`', ... , '/dev/null', 'CAk[S', '.shstrtab', '.init', '.text', '.fini', '.rodata', '.ctors', '.dtors', '.data', '.bss', '']
...
IoT malware hash: 1ec7746b189bfda654c2290033c25ab4c618abbee63a1bac7926b45f2f19d601.elf
String literals: ['TUPX!$', '3:?`3', ... ,  '$Info: This file is packed with the UPX executable packer http://upx.sf.net $', '$Id: UPX 3.96 Copyright (C) 1996-2020 the UPX Team. All Rights Reserved. $', '/proc/self/exe', '{{ p', 'proc/sel', 'f/exe\\n', "-76'", 'm0gpk', '\\6;>', 'Q{{_', '+]6K', ';CUP', '1lWT(', 'M@4_', '"Sl1', "L+=ko'", "g'O,", 'K[nWS', 'v74`', 'kPX4:', 'GCC: (G', 'NU) 3.', '2 200', 'ian pre', 'leas', 'KDJv', '_Unwind_', 'VRS_Get', '~Compl', 'ception', 'Text', '~DataC', '>For', '=ais', '\tthrow', '_Pop', 'cpp_', '2}N)', 'guage', 'Specific', 'SHtrt', '/ho<', '8nal', 'build/', 'gcc-c', 'ib1f', 'xcs.[', '| AS ', '7.5.K', '1`ZE', '754-df.Sa', '.g-[', '{<6H', ')=p,', '*_sH', 'GX(d.HXO', '`w\\N', 'Zb r', 'ps0#Hk', "~`'n", 'pvrs', '_rtcv', '5!GU', '%exc', ... , '@H@H!(', 'UPX!', '']

```

### Selection of IoT Malware Samples
**Command:**
```bash
mv STRINGS ../RESTRICT_EMBEDS/complete
cd ../RESTRICT_EMBEDS/
python3 RestrictToOldVersion.py
```
**Output:**
```console
Size before restriction STRINGS 200
Size after restriction STRINGS 157
```

### Clone Searches
**Command:**
```bash
mv final/STRINGS ../../XP/
cd ../../XP/
mkdir RS/
python3 RunSmallStringSet.py 
```

**Output:**
```console
\# of IoT malware 157
Starting Clone Searches
100%|████████████████████| 157/157 [00:01<00:00, 88.52it/s]
StringSet 1.7849047183990479 s
```

### Table Generation
**Command:**
```bash
cd ../Redaction/
python3 IoT_Small.py
```
**Output:**
```console
          AVG Clone Search (s) Precision Total Clone Search (s)
StringSet                0.01s     0.682                     2s
```

## PSSO on a Small Part of the Windows Dataset (7 minutes)

Replicate PSSO clone searches on a small part of the Windows dataset.

This example does not include the preprocessing phase, as the data is not available due to copyright issues.

### Clone Searches
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
100%|████████████████████| 200/200 [03:53<00:00,  1.17s/it]
6 PSSO 234.02400159835815 s
```

### Table Generation
**Command:**
```bash
cd ../Redaction/
python3 Windows_Small.py
```
**Output:**
```console
     AVG Clone Search (s) Precision Total Clone Search (s)
PSSO        1.56s (0.39s)     0.430          5h27m (5h23m)
```

## MutantX-S on the Clang v7/v4 Test Field of the BinKit Dataset (20 minutes)

Replicate MutantX-S clone searches on one cross-compiler test field.

This example does not include the preprocessing phase because the samples and disassembly files were too big to be included directly.

However, if you download BinKit samples [here](https://github.com/SoftSec-KAIST/BinKit) and place them into `BinKit/Normal/DataGeneration/samples/`, you can disassemble them using scripts inside `BinKit/Normal/DataGeneration` and perform MutantX-S preprocessing with `BinKit/Normal/DataGeneration/MUTANTX/Preprocess.py`. Be warned that this will take days.


### Clone Searches
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
clang-7.0/clang-4.0 7520 7520
100%|████████████████████| 7520/7520 [16:43<00:00,  7.50it/s]
clang-7.0/clang-4.0 1 MUTANTX2 1003.184271812439 s
```

### Table Generation
**Command:**
```bash
python3 ReadSmall.py
rm -r EMBEDS/
```
**Output:**
```console
MutantX-S results only on clang-7.0_VS_clang-4.0 in one direction.
MUTANTX2 clang-7.0_VS_clang-4.0 5931 7520 0.7886968085106383 0.13317347308422656
          AVG Clone Search (s) Precision Total Clone Search (s)
MutantX-S                0.13s     0.789                 16m41s
```
