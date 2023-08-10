## Basic Usage Example

```shell
conda activate PSS_Base
cd ../
python3 computesEmbeddings.py
```

This command will compute function embeddings for the subdataset UtilsOptions of the dataset Basic using a precomputed model for SAFE.

The command should display a tqdm progress bar ranging from 0 to 88.

It will take about half an hour to get every function embeddings from all 88 programs.

You can stop it at any moment and look at the files you have produced inside this folder.
