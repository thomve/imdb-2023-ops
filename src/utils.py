import json
import logging
import yaml

def load_config(filename):
    with open(filename, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            logging.error(exc)


def load_json(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        return data