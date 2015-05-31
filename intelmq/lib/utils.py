import logging
import json
import base64


def base64_decode(value):
    return base64.b64decode(value)


def base64_encode(value):
    return base64.b64encode(value)


def load_configuration(configuration_filepath):
    with open(configuration_filepath, 'r') as fpconfig:
        config = json.loads(fpconfig.read())
    return config


def log(logs_path, name, loglevel="DEBUG"):
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    
    handler = logging.FileHandler("%s/%s.log" % (logs_path, name))
    handler.setLevel(loglevel)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)    
    return logger
