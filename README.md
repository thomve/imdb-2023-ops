# A simple example of a MLOps pipeline

## Setup

Install the conda environment with:
```
conda env create -f etc/environment.yml
```
Then activate the environment with:
```
conda activate imdb
```

## Execution


### Configure DVC

```
dvc init
```

### Model training

```python
python src/prepare_data.py
```
Then:
```
dvc add <path_to_data>
```
Then
```
python src/train_model.py
```