# Artifact - Scalable Program Clone Search Through Spectral Analysis

## Abstract
We consider the problem of program clone search, i.e. given a target program and a repository of known programs (all in executable format), the goal is to find the program in the repository most similar to our target program – with potential applications in terms of reverse engineering, program clustering, malware lineage and software theft detection.

Recent years have witnessed a blooming in code similarity techniques, yet most of them focus on function-level similarity while we are interested in program-level similarity. 
Consequently, these recent approaches are not directly suited to program clone search, being either too slow to handle large code bases, not precise enough, or not robust against slight variations introduced by compilation or source code versions. 

We introduce Programs Spectral Similarity (PSS), the first spectral analysis dedicated to program-level similarity.
PSS reaches a sweet spot in terms of precision, speed and robustness. Especially, its one-time spectral feature extraction is tailored for large repositories of programs, making it a perfect fit for program clone search.

![Architecture of a Program Clone Search Procedure](./ArchitectureProgramCloneSearchProcedure.png "Architecture of a Program Clone Search Procedure")

## Download
In order to clone this repository, one needs git-lfs.
1. Install git-lfs https://www.atlassian.com/git/tutorials/git-lfs#installing-git-lfs
2. Type "git lfs clone git@github.com:sppunderreview/psso.git"

## Usage
One can produce Basic dataset LaTeX tables inside the "Results/" folder, using precomputed results disseminated into each framework folder.

### Basic dataset computation
Paths have to be corrected:
1. Inside benchmark core scripts such as "Basic/GCoreutilsOptions/makeBenchCO.py".
2. Inside scripts for frameworks, such as "MutantX-S/" folder.

Inside a framework folder:
* 'RunMakeMD3.py' computes all similarity indices.
* 'RunMakeMD.py'  use indices to compute test fields result.

### Some frameworks have a complex workflow
For instance, a function embedding requires a learning phase, embedding generation, and distance computation.

Only then should MDs be computed.

## Miscellaneous
- BinKit, IoT, and Windows datasets are not included. However, each program's embedding, and complete results are included.
- Disassembling requires IDA Pro under a Linux system.
- The Asm2vecJava folder contains the Java source code for Asm2Vec, while Asm2Vec contains results.
- Gencoding produces Gemini inputs from raw programs.

## Acknowledgments
This work is supported by (i) a public grant overseen by the French National Research Agency (ANR) as part of the "Investissements d'Avenir" French PIA project "Lorraine Université d'Excellence", reference ANR-15-IDEX-04-LUE, and (ii) has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 830927 (Concordia).

Experiments presented in this paper were carried out using the Grid'5000 experimental testbed, being developed under the INRIA ALADDIN development action with support from CNRS, RENATER and several Universities as well as other funding bodies (see https://www.grid5000.fr).

#
