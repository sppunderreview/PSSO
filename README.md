# A New Spectral Similarity for Scalable Program Clone Search
Anonymized Replication Package

# Download
In order to clone this repository, one needs git-lfs.
1. Install git-lfs https://www.atlassian.com/git/tutorials/git-lfs#installing-git-lfs
2. Type "git lfs clone git@github.com:sppunderreview/psso.git"

# Usage
One can produce Basic dataset LaTeX tables inside the "Results/" folder, using precomputed results disseminated into each framework folder.

## Basic dataset computation
Paths have to be corrected:
1. Inside benchmark core scripts such as "Basic/GCoreutilsOptions/makeBenchCO.py".
2. Inside scripts for frameworks, such as "MutantX-S/" folder.

Inside a framework folder:
* 'RunMakeMD3.py' computes all distances.
* 'RunMakeMD.py'  use distances to get test fields.

### Some frameworks have a complex workflow
For instance, a function embedding requires a learning phase, embedding generation, and distance computation.

Only then should MDs be computed.

## Miscellaneous
BinKit, IoT, and Windows datasets are not included. However, each program's embedding, and complete results are included.
Disassembling requires IDA Pro under a Linux system.
The Asm2vecJava folder contains the Java source code for Asm2Vec, while Asm2Vec contains results.
Gencoding produces Gemini inputs from raw programs.
