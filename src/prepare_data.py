import logging
import logging.config
import pandas as pd

from utils import load_config


def load_and_prepare_data(path_raw: str, path_processed: str):
    df = pd.read_csv(path_raw)
    df.set_index('id', inplace=True)
    df = df.dropna()

    df['release_date'] = pd.to_datetime(df['release_date'])

    df['net_profit'] = df['gross'] - df['budget']

    genres = df['genres'].str.get_dummies(sep = ',')

    sub = pd.DataFrame()
    sub[['originalTitle', 'net_profit']] = df[['originalTitle', 'net_profit']].copy()

    sub.set_index(df.index)
    sub = pd.concat([sub, genres], axis=1)

    sub_corr = sub.drop('originalTitle',axis = 1).corr()
    sub_corr['net_profit'].abs().sort_values(ascending = False)

    important_genres = sub_corr['net_profit'].abs().round(2).sort_values(ascending = False)[1:6].index

    df = df[['isAdult', 'runtimeMinutes', 'averageRating', 'numVotes', 'budget', 'gross', 'release_date', 'net_profit', 'directors']]

    df['release_year'] = df['release_date'].dt.year
    df['release_month'] = df['release_date'].dt.month
    df['release_day'] = df['release_date'].dt.day

    df = df.drop('release_date', axis = 1)

    df = pd.concat([df, genres[important_genres]], axis=1)

    directors = df['directors'].str.get_dummies(sep=',').add_prefix('Director_')

    director_corr = pd.concat([df['net_profit'], directors], axis=1).corr()
    important_directors = director_corr['net_profit'].abs().sort_values(ascending = False)[1:15].index

    df = pd.concat([df, directors[important_directors]], axis=1)
    df = df.drop('directors', axis = 1)

    df.to_csv(path_processed)
    

if __name__ == "__main__":
    logging.config.fileConfig('logging.conf')
    config = load_config('etc/config.yml')
    load_and_prepare_data(config['data']['raw']['path'], config['data']['processed']['path'])