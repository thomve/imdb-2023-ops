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

### Model training

```python
python src/load_and_prepare_data.py
```
Then
```
python src/train_model.py
```