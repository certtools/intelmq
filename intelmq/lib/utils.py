import logging
import json
import base64


def decode(text, encodings=["utf-8"], force=False):
    if type(text) is unicode:
        return text

    for encoding in encodings:
        try:
            return text.decode(encoding)
        except ValueError as e:
            pass
        
    if force:
        for encoding in encodings:
            try:
                return text.decode(encoding, 'ignore')
            except ValueError as e:
                pass

    raise Exception("Found a problem when decoding.")

def encode(text, encodings=["utf-8"], force=False):
    for encoding in encodings:
        try:
            return text.encode(encoding)
        except ValueError as e:
            pass
        
    if force:
        for encoding in encodings:
            try:
                return text.decode(encoding, 'ignore')
            except ValueError as e:
                pass

    raise Exception("Found a problem when encoding.")

def base64_decode(value):
    data =  base64.b64decode(value)
    _data = data.decode('utf-8', 'ignore')
    return _data.encode('utf-8')

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
