from os.path import dirname, join
import tempfile

directory = dirname(__file__)
cert_dir = "certs"

certs = join(directory, cert_dir)

APPCERT = join(certs, "app.crt")
APPKEY  = join(certs, "app.key")

RECEIVERCERT = join(certs, "receiver.crt")
RECEIVERKEY = join(certs, "receiver.key")

TMPDIR = join(tempfile.gettempdir(), "tmp_deployer")

STATIC_PATH = join(dirname(__file__), "static")

TOMCAT_PATH = '/var/lib/tomcat7/webapps/'

DEPLOYER_PORT = 1342
RECEIVER_PORT= 1339
RECEIVER_WEBSOCKET_PORT = 1370

PIDFILE_DEPLOYER = '/var/run/marcopolo/deployer.pid'
PIDFILE_RECEIVER = '/var/run/marcopolo/receiver.pid'
