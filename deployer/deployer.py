#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.web
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado import web, websocket, ioloop, template
from tornado.httpserver import HTTPServer
from pyjade.ext.tornado import patch_tornado

import os
import random, string

patch_tornado()

import sys
sys.path.append('/opt/marcopolo/') #Temporary fix to append the path

from bindings.marco import marco
from marco_conf.utils import Node
import utils

import json
import requests, mimetypes
from tempfile import tempdir
import tempfile
import ssl, conf
from requests.adapters import HTTPAdapter 


class NotCheckingHostnameHTTPAdapter(HTTPAdapter):
	"""
	A middleware that avoids the verification of the SSL Hostname field.
	Due to the fact that the name of the client cannot be verified,
	it is simply not checked
	"""
	def cert_verify(self, conn, *args, **kwargs):
		"""
		Avoids the verification of the SSL Hostname field 
		"""
		super().cert_verify(conn, *args, **kwargs)
		conn.assert_hostname = False


websession = requests.session()
websession.mount('https://', NotCheckingHostnameHTTPAdapter()) # By changing the adapter no hostname is checked

#Creation of the directory if it does not exists
if not os.path.exists(conf.TMPDIR):
	os.makedirs(conf.TMPDIR)

__UPLOADS__ = conf.TMPDIR # tmp directory were files will be stored

open_ws = set()

class BaseHandler(tornado.web.RequestHandler):

	def get_current_user(self):
		"""
		Decrypts the secure cookie
		"""
		return self.get_secure_cookie("user")

class IndexHandler(BaseHandler):
	"""
	In charge of handling GET requests. Provides the client with the necessary .html/css/js
	"""
	@web.addslash
	def get(self):
		
		if not self.current_user:
			self.redirect("/login")
		else:
			user = tornado.escape.xhtml_escape(self.current_user)
			self.render("templates/index.jade", user=user)
			


class LoginHandler(BaseHandler):
	"""
	Handles login authentication through cookies
	"""
	def get(self):
		if self.current_user:
			self.redirect("/")
		else:
			self.render("templates/login.jade")

	def post(self):

		if utils.authenticate(self.get_argument("name"), self.get_argument("pass")):
			self.set_secure_cookie("user", self.get_argument("name"))
		else:
			self.set_status(403)
			self.finish("")
		self.redirect("/")

class Logout(BaseHandler):
	def get(self):
		self.clear_cookie("user")
		self.redirect("/")

class UploadAndDeployHandler(BaseHandler):
	"""
	Listens for POSTs requests and performs the deployment asynchronously
	"""
	@tornado.web.asynchronous #The post is asynchronous due to the potencially long deploying response time
	@tornado.gen.engine
	def post(self):
		file1 = self.request.files['file'][0] #Only one file at a time

		original_fname = file1['filename']
		print(os.path.join(__UPLOADS__, original_fname))
		output_file = open(os.path.join(__UPLOADS__, original_fname), 'wb')
		output_file.write(file1['body'])
		output_file.close()
		# The nodes are returned as a comma-separated string
		nodes = self.get_argument('nodes', '').split(',')[:-1] 
		from concurrent import futures
		
		#The deployment process is performed asynchronously using a ThreadPool, which will handle the request asynchronously
		thread_pool = futures.ThreadPoolExecutor(max_workers=len(nodes))
		
		@tornado.gen.coroutine
		def call_deploy(node):
			yield thread_pool.submit(self.deploy, node=node, request=self, filename=original_fname, command=self.get_argument('command', ''), user=self.current_user, tomcat=self.get_argument('tomcat', ''))
		
		for node in nodes:
			deployment = tornado.gen.Task(call_deploy, node)
		
		self.finish("file" + original_fname + " is uploaded and on deploy")
	
	@tornado.web.asynchronous
	def deploy(self, node, request, filename, command, user, folder="", idpolo="", tomcat=""):
		
		
		def get_content_type(filename):
			return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

		url = "https://"+node+":"+str(conf.RECEIVER_PORT)+"/deploy"
		files = {'file': (filename, open(os.path.join(__UPLOADS__, filename), 'rb'), get_content_type(filename))}
		commands = {'command':command, 'user':user, 'folder': folder, 'idpolo': idpolo, 'tomcat': tomcat}
		
		r = websession.post(url, files=files, data=commands, verify=conf.RECEIVERCERT, cert=(conf.APPCERT, conf.APPKEY))
		
class NodesHandler(websocket.WebSocketHandler):
	"""
	Handler for the Polo websocket connection
	"""
	#polo will have events to notify of new nodes. New crazy idea...
	def check_origin(self, origin):
		return True

	def open(self):
		open_ws.add(self)
		m = marco.Marco()
		try:
			nodes = m.request_for("deployer")
			self.write_message(json.dumps({"Nodes":[n.address[0] for n in nodes]}))
		except marco.MarcoTimeOutException:
			self.write_message(json.dumps({"Error": "Error in marco detection"}))
		 		
	def send_data(self):
		pass

	def on_close(self):
		pass

	def send_update(self):
		pass


routes = [
	(r'/', IndexHandler),
	(r'/static/(.*)', StaticFileHandler, {"path":"./static"}),
	(r'/ws/nodes', NodesHandler),
	(r"/login", LoginHandler),
    (r"/logout", Logout),
	(r'/upload', UploadAndDeployHandler),
]

settings = {
	"debug": True,
    "static_path": conf.STATIC_PATH,
    "login_url":"/login" , 
    "cookie_secret":"2a70b29a80c23f097a074626e584c8f60a87cf33f518f0eda60db0211c82"
}

app = Application(routes, **settings)

if __name__ == "__main__":
	
	"""ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
	ssl_ctx.load_cert_chain(os.path.join("/home/martin/TFG/workspaces/deployer/cert/certs", "receiver.crt"),
                        os.path.join("/home/martin/TFG/workspaces/deployer/cert/certs", "receiver.key"))
	ssl_ctx.verify_mode = ssl.CERT_OPTIONAL
	#ssl_ctx.ssl_version = ssl.PROTOCOL_TLSv1
	#ca_certs = os.path.join("/home/martin/TFG/workspaces/deployer/cert/certs", "app.crt")
	#ssl_ctx.ca_certs = os.path.join("/home/martin/TFG/workspaces/deployer/cert/certs", "app.crt")
	"""
	#TODO Replace with SSLContext (this option is maintained for compatibility reasons)
	httpServer = HTTPServer(app, ssl_options={ 
        "certfile": conf.APPCERT,
        "keyfile": conf.APPKEY,
        "cert_reqs": ssl.CERT_OPTIONAL,
        "ssl_version": ssl.PROTOCOL_TLSv1,
        #"ca_certs": conf.RECEIVERCERT,
    })

	httpServer.listen(conf.DEPLOYER_PORT)
	ioloop.IOLoop.instance().start()

	"""Multicore:def main():
	app = make_app()
	server = tornado.httpserver.HTTPServer(app)
	server.bind(8888)
	server.start(0)  # forks one process per cpu
	IOLoop.current().start()"""