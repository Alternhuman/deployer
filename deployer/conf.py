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

DEPLOYER_PORT = 1341
RECEIVER_PORT= 1339