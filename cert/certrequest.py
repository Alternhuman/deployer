#!/usr/bin/env python3
# -*- coding: utf-8
from tornado.web import RequestHandler, Application, asynchronous, \
                        StaticFileHandler
from tornado.httpserver import HTTPServer
from tornado.log import app_log, gen_log
from tornado.ioloop import IOLoop
import ssl
from os import path
import os



current_dir = os.path.dirname(__file__)
certdir = os.path.join(current_dir, "certs")

class HandleRequest(RequestHandler):
	def post(self):
		print(self.get_argument('key1'))
		self.write("OK")


application = Application([
	(r'/', HandleRequest),
])

if __name__ == "__main__":
	http_server = HTTPServer(application, ssl_options={
        "certfile": os.path.join(certdir, "receiver.crt"),
        "keyfile": os.path.join(certdir, "receiver.key"),
        "cert_reqs": ssl.CERT_OPTIONAL,
        "ssl_version": ssl.PROTOCOL_TLSv1,
        "ca_certs": os.path.join(certdir, "app.crt"),
    })
	http_server.listen(9001, address='0.0.0.0')
	try:
		IOLoop.instance().start()
	except KeyboardInterrupt:
		pass
"""#!/usr/bin/env python3
# -*- coding: utf-8
from tornado.web import RequestHandler, Application, asynchronous, \
                        StaticFileHandler
from tornado.httpserver import HTTPServer
from tornado.log import app_log, gen_log
from tornado.ioloop import IOLoop
import ssl
from os import path
import os



current_dir = os.path.dirname(__file__)
certdir = os.path.join(current_dir, "certs")

class HandleRequest(RequestHandler):
	def post(self):
		print(self.get_argument('key1'))
		self.write("OK")


application = Application([
	(r'/', HandleRequest),
])

if __name__ == "__main__":
	http_server = HTTPServer(application, ssl_options={
        "certfile": os.path.join(certdir, "minion.pem"),
        "keyfile": os.path.join(certdir, "minion.key"),
        "cert_reqs": ssl.CERT_OPTIONAL,
        "ssl_version": ssl.PROTOCOL_TLSv1,
        "ca_certs": os.path.join(certdir, "malote.pem"),
    })
	http_server.listen(9001, address='0.0.0.0')
	try:
		IOLoop.instance().start()
	except KeyboardInterrupt:
		pass"""