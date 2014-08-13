import shutil
import urllib2
import StringIO
from intelmq.lib.utils import decode

def fetch_url(url, timeout=60.0, chunk_size=16384):
    req = urllib2.urlopen(url, timeout = timeout)
    strio = StringIO.StringIO()
    shutil.copyfileobj(req, strio, chunk_size)
    value = strio.getvalue()
    strio.close()
    return decode(value, force=True)