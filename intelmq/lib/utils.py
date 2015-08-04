import logging
import json
import base64
import os


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


def reverse_readline(filename, buf_size=8192):
    """a generator that returns the lines of a file in reverse order
    http://stackoverflow.com/a/23646049/2851664"""
    with open(filename) as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        total_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(total_size, offset + buf_size)
            fh.seek(-offset, os.SEEK_END)
            buffer = fh.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split('\n')
            # the first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # if the previous chunk starts right from the beginning of line
                # do not concact the segment to the last line of new chunk
                # instead, yield the segment first
                if buffer[-1] is not '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if len(lines[index]):
                    yield lines[index]
        yield segment
