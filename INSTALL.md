# Installation Instructions

Follow the steps below to install and set up the artifact:

## 0. Install Conda
If you don't have Conda, you can install it by following the instructions [on the Conda website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).

## 1. Install Software Packages
```shell
sudo apt install git
sudo apt install git-lfs
sudo apt install binutils
sudo apt install zip
```

If you have troubles installing git-lfs see the instructions [on the git-lfs repository](https://github.com/git-lfs/git-lfs/blob/main/INSTALLING.md).

## 2. Download the Repository

1. Navigate to the desired directory where you want to download the repository.
2. Clone the repository using Git Large File Storage (LFS):

   ```shell
   git lfs clone git@github.com:sppunderreview/psso.git
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

## Basic Usage Example

To confirm that the artifact is installed and working, follow the steps below:

```shell
conda activate PSS_Base
cd SAFE/makeEmbeds/
python3 computesEmbeddings.py
```

The output of the above command should display a `tqdm` progress bar ranging from 0 to 88.
This command will compute SAFE function embeddings for the dataset "UtilsOptions" of "Basic" using the SAFE precomputed model.
It should output files inside `SAFE/makeEmbeds/UO` folder.

## Software for Asm2Vec
To reproduce Asm2Vec experiments, you will need Eclipse IDE with JDK 11.

You can install it by following the instructions [on the Eclipse website]( https://eclipseide.org/).


