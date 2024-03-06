import logging
import logging.config
import numpy as np
import pandas as pd
import xgboost as xgb

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


from utils import load_config, load_json



def compute_rmse(y: np.array, y_pred: np.array):
    return np.sqrt(mean_squared_error(y, y_pred))


def train_model(path_data: str, path_model: str, path_model_param: str):
    df = pd.read_csv(path_data)

    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

    target = 'net_profit'
    features_list = ['isAdult', 'runtimeMinutes', 'averageRating', 'numVotes', 'budget', 'release_year', 'release_month', 'release_day', 'Adventure', 'Animation', 'Drama', 'Action', 'Crime', 'Director_James Cameron', 'Director_ Joe Russo', 'Director_Anthony Russo', 'Director_Jon Watts', 'Director_ Jennifer Lee', 'Director_Chris Buck', 'Director_Pierre Coffin', 'Director_David Yates', 'Director_Peter Jackson', 'Director_Joss Whedon', 'Director_J.J. Abrams', 'Director_Colin Trevorrow', 'Director_ Pierre Leduc', 'Director_ Michael Jelenic']
    dtrain = xgb.DMatrix(df_train[features_list], label=df_train[target])
    dtest = xgb.DMatrix(df_test[features_list], label=df_test[target])

    # train the model
    param = load_json(path_model_param)
    evallist = [(dtrain, 'train'), (dtest, 'eval')]
    num_round = 100
    bst = xgb.train(param, dtrain, num_round, evallist)
    bst.save_model(path_model)

    # evaluate model
    df_test[target + '_pred'] = bst.predict(dtest)
    rmse_test = compute_rmse(df_test[target], df_test[target + '_pred'])
    logging.info("RMSE on test dataset: %s", rmse_test)


if __name__ == "__main__":
    logging.config.fileConfig('logging.conf')
    config = load_config('etc/config.yml')
    train_model(config['data']['processed']['path'], 
                config['model']['path'],
                config['model']['path_param'])