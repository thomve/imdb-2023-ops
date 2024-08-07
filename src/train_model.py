import logging
import logging.config
import mlflow
import numpy as np
import pandas as pd
import xgboost as xgb

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from utils import load_config, load_json


def compute_rmse(y: np.array, y_pred: np.array):
    """
    Compute the root mean squared error (RMSE) between the true values (y) and the predicted values (y_pred).

    Parameters:
    y (np.array): Array of true values.
    y_pred (np.array): Array of predicted values.

    Returns:
    float: The root mean squared error (RMSE) between y and y_pred.
    """
    return np.sqrt(mean_squared_error(y, y_pred))

def setup_mlflow_experiment(experiment_name: str):
    """
    Sets up an MLflow experiment with the given experiment name.

    Parameters:
    experiment_name (str): The name of the experiment.

    Returns:
    int: The ID of the experiment.

    """
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment:
        logging.info(f"Experiment '{experiment_name}' already exists (ID: {experiment.experiment_id})")
        return experiment.experiment_id
    else:
        experiment_id = mlflow.create_experiment(experiment_name)
        logging.info(f"Created new experiment '{experiment_name}' with ID: {experiment_id}")
        return experiment_id

def train_model(config):
    """
    Trains an XGBoost model using the provided configuration.

    Args:
        config (dict): A dictionary containing the configuration parameters.

    Returns:
        None
    """
    mlflow.set_tracking_uri(config['mlflow']['backend_store_path'])
    eid = setup_mlflow_experiment(experiment_name="imdb-2023")
    with mlflow.start_run(experiment_id=eid):
        df = pd.read_csv(config['data']['processed']['path'])
        df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

        target = 'net_profit'
        features_list = ['isAdult', 'runtimeMinutes', 'averageRating', 'numVotes', 'budget', 'release_year', 'release_month', 'release_day', 'Adventure', 'Animation', 'Drama', 'Action', 'Crime']
        dtrain = xgb.DMatrix(df_train[features_list], label=df_train[target])
        dtest = xgb.DMatrix(df_test[features_list], label=df_test[target])

        # train the model
        params = load_json(config['model']['path_param'])
        mlflow.log_params(params)
        evallist = [(dtrain, 'train'), (dtest, 'eval')]
        num_round = 100
        bst = xgb.train(params, dtrain, num_round, evallist)
        bst.save_model(config['model']['path'])
        mlflow.xgboost.log_model(xgb_model=bst, artifact_path='xgb-model-01')

        # evaluate model
        df_test[target + '_pred'] = bst.predict(dtest)
        rmse_test = compute_rmse(df_test[target], df_test[target + '_pred'])
        mlflow.log_metric("rmse_test", rmse_test)
        logging.info("RMSE on test dataset: %s", rmse_test)


if __name__ == "__main__":
    logging.config.fileConfig('logging.conf')
    config = load_config('etc/config.yml')
    train_model(config)