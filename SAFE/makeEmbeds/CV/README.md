## Basic Usage Example

```shell
conda activate PSS_Base
cd ../
python3 computesEmbeddings.py
```

This command will compute function embeddings for the subdataset CoreutilsVersions of the dataset Basic using a precomputed model for SAFE.

The command should display a tqdm progress bar ranging from 0 to 348.

It will take about five minutes to get every function embeddings from all programs.

You can stop it at any moment and look at the files you have produced inside this folder.
