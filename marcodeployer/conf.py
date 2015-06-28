from os.path import dirname, join
import tempfile

directory = dirname(__file__)
cert_dir = "/usr/lib/marcodeployer/certs"

certs = join(directory, cert_dir)

APPCERT = join(certs, "app.crt")
APPKEY  = join(certs, "app.key")

RECEIVERCERT = join(certs, "receiver.crt")
RECEIVERKEY = join(certs, "receiver.key")

TMPDIR = join(tempfile.gettempdir(), "tmp_deployer")

#STATIC_PATH = join(dirname(__file__), "static")
STATIC_PATH = "/usr/lib/marcodeployer/static"

TOMCAT_PATH = '/var/lib/tomcat7/webapps/'

DEPLOYER_PORT = 1342
RECEIVER_PORT = 1339
RECEIVER_WEBSOCKET_PORT = 1370

PIDFILE_DEPLOYER = '/var/run/marcodeployerd.pid'
PIDFILE_RECEIVER = '/var/run/marcoreceiverd.pid'

INTERFACE='eth0'

REFRESH_FREQ = 1000.0

STATUS_MONITOR_SERVICE_NAME = "statusmonitor"
DEPLOYER_SERVICE_NAME = "deployer"
RECEIVER_SERVICE_NAME = "receiver"

TEMPLATES_DIR = "/usr/lib/marcodeployer/templates/"

LOGGING_DIR = "/var/log/marcopolo"
DEPLOYER_LOG_FILE = "/var/log/marcodeployer/marcodeployerd"
RECEIVER_LOG_FILE = "/var/log/marcodeployer/marcoreceiverd"

DEPLOYER_LOGLEVEL = "DEBUG"
RECEIVER_LOGLEVEL = "DEBUG"