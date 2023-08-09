# Artifact - Scalable Program Clone Search Through Spectral Analyss

The artifact is a purposely-built framework for clone search method comparison.

It is easily extensible and can be tweaked to carry out new measurements.

## Requirements

This artifact requires a storage capacity of 130 GB and a computer with a Debian system.

Disassembling binaries, which is optional, requires IDA Pro with a version close to 7.5.

For additional details, please consult `REQUIREMENTS.md`.

## Installation

In order to clone this repository, you will need git-lfs first, please refer to `INSTALL.md`.

## Example of Use

1. Activate the environment with `conda activate PSS_Base`
2. Run `python3 MakeTables.py` 

The above will produce Tables of the Camera Ready version of our article using precomputed results.

## Usage - Basic
For Basic dataset computation, ensure you have run SetAbsolutePath.py.

Inside a method folder:
- `RunMakeMD3.py` will compute all similarity indices using precomputed features.
- `RunMakeMD.py` will utilize these indices to compute the test field results.

To reproduce the feature extraction, a script usually called "Preprocess.py" can be runned.

Some frameworks have a more complex workflow. For instance, a function embedding requires a learning phase, embedding computations, and distance computations (`gDist` folders), only after should similarity indices be computed.


## Usage - BinKit 
The `BinKit/` directory has two subdirectories, namely, `Obfus`, which deals with obfuscated programs, and `Normal`. 
Each subdirectory entails a `DataGeneration` folder which holds the disassembly scripts, and a unique folder for each method.
These method folders have scripts to extract features and embeds from samples.

Each subdirectory contains three significant scripts:
1. `Run.py`: This script reproduces clone searches using precomputed embeddings in folders like `NORMAL_EMBEDS_2`.
2. `Read.py`: It convert the results into a readable output.
3. `ReadElapsed.py`: It converts the results into a dictionary storing running times.

The `Redaction` subdirectory within `BinKit/` holds scripts that compute tables based on results obtained within each subdataset.

## Usage - IoT and Windows
Both `IoT/` and `Windows/` folders contain a `DataGeneration/` subdirectory with disassembly scripts and scripts for each method to extract features and embeddings from samples. 
Additionally, each dataset has a `DataLabelling/` subdirectory which contains scripts for labeling data. 

Experiment folders such as  `XP/`  include `Run.py` scripts for conducting clone searches using precomputed embeddings. 
Lastly, the `Redaction` subdirectory in each dataset includes scripts for computing tables from the results of experiment folders.


## Content Overview

### Software 

The artifact includes implementations of 21 distinct clone search methods, comprising 6 new methods and 15 methods adapted or reimplemented from preceding works in the field.

### Data Repositories 

The artifact features four datasets:
- The `Basic/` folder holds comprehensive data of a thousand programs. It includes source code, disassembly files, and features.
- The `IoT/` folder holds twenty thousand malware taken from  [MalwareBazaar](https://bazaar.abuse.ch/), plus scripts for selecting, downloading, and labelling the data, along with all disassembly files and features.
- Due to size constraints and copyright issues respectively, complete disassembly files and software aren't included inside `BinKit/` and `Windows/` folders. However, setup for disassembly and feature extraction reproduction is included. The BinKit dataset is readily accessible [here](https://github.com/SoftSec-KAIST/BinKit).

## Corrections
We have corrected two measurements in the Camera Ready version of our article:
- We had to multiply the preprocessing time of PSS, PSSO and ASCG by 3 on the Basic dataset (see `Basic/Redaction/Speed/README.md` for more details).
- We had to correct the preprocessing time of PSS and ASCG on 63 large programs on the Windows dataset (see `Windows/Redaction/README.md` for more details).


## Abstract
We consider the problem of program clone search, i.e. given a target program and a repository of known programs (all in executable format), the goal is to find the program in the repository most similar to our target program – with potential applications in terms of reverse engineering, program clustering, malware lineage and software theft detection.

Recent years have witnessed a blooming in code similarity techniques, yet most of them focus on function-level similarity while we are interested in program-level similarity. 
Consequently, these recent approaches are not directly suited to program clone search, being either too slow to handle large code bases, not precise enough, or not robust against slight variations introduced by compilation or source code versions. 

We introduce Programs Spectral Similarity (PSS), the first spectral analysis dedicated to program-level similarity.
PSS reaches a sweet spot in terms of precision, speed and robustness. Especially, its one-time spectral feature extraction is tailored for large repositories of programs, making it a perfect fit for program clone search.

![Architecture of a Program Clone Search Procedure](./ArchitectureProgramCloneSearchProcedure.png "Architecture of a Program Clone Search Procedure")

## Acknowledgments

This work is supported by (i) a public grant overseen by the French National Research Agency (ANR) as part of the "Investissements d'Avenir" French PIA project "Lorraine Université d'Excellence", reference ANR-15-IDEX-04-LUE, and (ii) has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 830927 (Concordia).

Experiments presented in this paper were carried out using the Grid'5000 experimental testbed, being developed under the INRIA ALADDIN development action with support from CNRS, RENATER and several Universities as well as other funding bodies (see https://www.grid5000.fr).
