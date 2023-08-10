## Basic Usage Example

```shell
conda activate PSS_Base
cd ../
python3 computesEmbeddings.py
```

The output of the above command should display a `tqdm` progress bar ranging from 0 to 88.
This command will compute SAFE function embeddings for the subdataset UtilsOptions of the dataset Basic using the SAFE precomputed model.
It should output files inside this folder.
