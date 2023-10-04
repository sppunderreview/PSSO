# Installation Instructions

Follow the steps below to install and set up the artifact:

## 0. Install Conda
If you don't have Conda, you can install it by following the instructions [on the Conda website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).

## 1. Install Software Packages
```shell
sudo apt install binutils
sudo apt install zip
sudo apt install p7zip
```


## 2. Download the Repository

### Download with Zenodo (Recommanded)

1. Navigate to the desired directory where you want to download the repository.
2. Download every file (archive) of the Zenodo record [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8289599.svg)](https://doi.org/10.5281/zenodo.8289599). 
3. Extract each archive.
4. Combine all PSSO folders within each archive into a unique PSSO folder.
5. Initialize paths:
   ```shell
   cd PSSO/
   python3 SetAbsolutePath.py
   ```

### Download with Git LFS (Legacy)

1. Download Git LFS:

   ```shell
   sudo apt install git
   sudo apt install git-lfs
   ```
   If you have trouble installing Git LFS see the instructions [on the git-lfs repository](https://github.com/git-lfs/git-lfs/blob/main/INSTALLING.md).

3. Navigate to the desired directory where you want to download the repository. 
4. Clone the repository using Git LFS:
   ```shell
   git lfs clone https://github.com/sppunderreview/PSSO.git
   cd PSSO/
   python3 SetAbsolutePath.py
   ```

## 3. Setup Conda Environments

### Main Environment (PSS_Base)
```shell
conda create --name PSS_Base --file requirements_PSS_Base.txt
conda activate PSS_Base
pip3 install opencv-python
pip3 install scann
pip3 install lapjv
pip3 install capstone
pip3 install matplotlib
pip3 install scikit-learn
pip3 install statsmodels
pip3 install pandas
pip3 install tqdm
pip3 install h5py
pip3 install requests
pip3 install editdistance
pip3 install angr
pip3 install gensim==3.8.0
```

### Gemini Environment (PSS_Gemini)
An optional environment to run Gemini tensorflow network.
```shell
conda create --name PSS_Gemini --file requirements_PSS_Gemini.txt
conda activate PSS_Gemini
pip3 install tensorflow==1.4.0
pip3 install matplotlib
pip3 install scikit-learn
pip3 install tqdm
```

### Gencoding Environment (PSS_Gencoding)
An optional environment to run Gencoding which disassembles programs and outputs Gemini network inputs.
```shell
conda create --name PSS_Gencoding --file requirements_PSS_Gencoding.txt
```

## Usage Example

To confirm that the artifact is installed and working, follow the steps below:

1. Activate the environment with `conda activate PSS_Base`
2. Run `python3 MakeTables.py`

The above will produce in a few minutes the Tables of the Camera Ready version of our article using precomputed results.

**Output**
```
Loading the Preliminary Evaluation Table ...
Table (Preliminary Evaluation) Total runtimes on the Basic dataset
               Total
Bsize             6s
Dsize             5s
Shape          1m22s
ASCG           1h18m
ASCFG        127h52m
GED-0         81h22m
MutantX-S         4s
Asm2vec      141h20m
Gemini       102h45m
SAFE         655h51m
PSS            1h18m
PSSO           15m9s
GED-L         46h57m
SMIT         3634h5m
CGC          171h57m
AlphaDiff    642h59m
LibDX           1m4s
LibDB         16h28m
StringSet        38s
FunctionSet       3s

...

Table (RQ3) Average rank-biserial correlation for H on the Basic dataset.
                              CO              UO              BO         Average
Bsize              \textbf{0.07}   \textbf{0.03}  \textbf{-0.04}   \textbf{0.02}
Dsize              \textbf{0.02}   \textbf{0.06}  \textbf{-0.04}   \textbf{0.01}
Shape              \textbf{0.10}   \textbf{0.06}  \textbf{-0.04}   \textbf{0.04}
ASCG                      {0.19}   \textbf{0.08}  \textbf{-0.04}   \textbf{0.08}
ASCFG                     {0.30}          {0.17}  \textbf{-0.02}   \textbf{0.15}
GED-0                     {0.25}   \textbf{0.05}  \textbf{-0.04}   \textbf{0.09}
MutantX-S                 {0.63}          {0.28}   \textbf{0.08}          {0.33}
Asm2vec                   {1.00}          {0.65}          {0.45}          {0.70}
Gemini                    {0.96}          {0.37}   \textbf{0.06}          {0.46}
SAFE                      {0.98}          {0.38}   \textbf{0.11}          {0.49}
PSS                \textbf{0.13}   \textbf{0.09}  \textbf{-0.02}   \textbf{0.07}
PSSO               \textbf{0.12}   \textbf{0.09}  \textbf{-0.02}   \textbf{0.06}
GED-L                     {0.21}   \textbf{0.08}  \textbf{-0.04}   \textbf{0.08}
SMIT              \textbf{-0.57}  \textbf{-0.44}  \textbf{-0.07}  \textbf{-0.36}
CGC                       {0.32}   \textbf{0.07}  \textbf{-0.08}   \textbf{0.10}
AlphaDiff                 {0.93}          {0.33}   \textbf{0.11}          {0.46}
LibDX             \textbf{-0.02}  \textbf{-0.16}  \textbf{-0.05}  \textbf{-0.08}
LibDB_Robustness          {0.46}          {0.22}  \textbf{-0.03}          {0.22}
StringSet                 {0.86}          {0.31}          {0.18}          {0.45}
FunctionSet               {0.37}          {0.22}   \textbf{0.02}          {0.20}


All Tables generated in 101.85 s
```

See [EXAMPLES.md](EXAMPLES.md) for five quick examples of replications using this artifact.

## Software for Asm2Vec
To fully reproduce Asm2Vec experiments, you will need Eclipse IDE with JDK 11.

You can install it by following the instructions [on the Eclipse website]( https://eclipseide.org/).


