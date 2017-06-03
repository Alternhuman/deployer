import six
import os
from six.moves import configparser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(BASE_DIR, 'build')
CONF_FILE_SEARCHPATHS = ['/etc/monitor', os.getcwd(), 
os.path.dirname(os.path.abspath(__file__))]

CONF_FILE_NAME = 'monitor.conf'

PORT = 9999
DEBUG = False
COOKIE_SECRET = "2a70b29a80c23f097a074626e584c8f60a87cf33f518f0eda60db0211c82"
REFRESH_FREQUENCY = 1000
XHEADERS = False

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

default_values = {
    "PORT": PORT,
    "DEBUG": DEBUG,
    "STATIC_PATH": STATIC_PATH,
    "COOKIE_SECRET": COOKIE_SECRET,
    "REFRESH_FREQUENCY": REFRESH_FREQUENCY,
    "XHEADERS": XHEADERS
}

for fn in map(lambda x: os.path.join(x, CONF_FILE_NAME), CONF_FILE_SEARCHPATHS): 
    if os.path.isfile(fn):
        try:
            config = configparser.SafeConfigParser(default_values, allow_no_value=False)

            with open(fn, 'r') as f:
                config.readfp(f)
                PORT = config.getint('http', 'port')
                XHEADERS = config.getboolean('http', 'xheaders')
                DEBUG = config.getboolean('app', 'debug')
                STATIC_PATH = config.get('app', 'static_path')
                COOKIE_SECRET = config.get('app', 'cookie_secret')
                REFRESH_FREQUENCY = config.getint('app', 'refresh_frequency')
            break
        except IOError as i:
            print("Warning! The configuration file could not be read. Defaults will be used as fallback")
            #logging.warning("Warning! The configuration file could not be read. Defaults will be used as fallback")
        except Exception as e:
            print("Unknown exception in configuration parser %s" % e)
            #logging.warning("Unknown exception in configuration parser %s" % e)

app_settings = {
    "debug": DEBUG,
    "static_path": STATIC_PATH,
    "login_url":"/login/",
    "cookie_secret": COOKIE_SECRET
    "xheaders": XHEADERS
}