#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.web
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado import web, websocket, ioloop, template
from tornado.httpserver import HTTPServer
from pyjade.ext.tornado import patch_tornado

import os, random, string, json, mimetypes, ssl, conf
from tempfile import tempdir
import tempfile

import sys
sys.path.append('/opt/marcopolo/') #Temporary fix to append the path

from bindings.marco import marco
from marco_conf.utils import Node
import utils

import requests
from requests.adapters import HTTPAdapter 

patch_tornado() #Allows pyjade to work with Tornado

import signal
from os import path, makedirs

class NotCheckingHostnameHTTPAdapter(HTTPAdapter):
	"""
	A middleware that avoids the verification of the SSL Hostname field.
	Since the name of the client cannot be verified,
	it is simply not checked
	From Juan Luis Boya
	"""
	def cert_verify(self, conn, *args, **kwargs):
		"""
		Avoids the verification of the SSL Hostname field 
		"""
		super().cert_verify(conn, *args, **kwargs)
		conn.assert_hostname = False


websession = requests.session()
websession.mount('https://', NotCheckingHostnameHTTPAdapter()) # By changing the adapter no hostname is checked

from requests_futures.sessions import FuturesSession
futures_session = FuturesSession()
futures_session.mount('https://', NotCheckingHostnameHTTPAdapter())

#Creation of the temporal directory if it does not exists
if not os.path.exists(conf.TMPDIR):
	os.makedirs(conf.TMPDIR)

__UPLOADS__ = conf.TMPDIR # tmp directory were files will be stored

open_ws = set()

#TODO
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
	@web.addslash #Appends a '/'
	def get(self):
		
		if not self.current_user:
			self.redirect("/login")
		else:
			user = tornado.escape.xhtml_escape(self.current_user)
			self.render("templates/index.jade", user=user)
			


class LoginHandler(BaseHandler):
	"""
	Handles login authentication through secure cookies and PAM
	"""
	def get(self):
		if self.current_user:
			self.redirect("/")
		else:
			self.render("templates/login.jade")

	def post(self):

		if utils.authenticate(self.get_argument("name"), self.get_argument("pass")):
			self.set_secure_cookie("user", self.get_argument("name"))
			self.redirect("/")
		else:
			self.set_status(403) #TODO
			self.finish("")

class Logout(BaseHandler):
	"""
	Removes the secure cookie
	"""
	def get(self):
		self.clear_cookie("user")
		self.redirect("/")

class UploadAndDeployHandler(BaseHandler):
	from tornado.gen import engine
	"""
	Listens for POST requests and performs the deployment asynchronously
	"""
	@tornado.web.asynchronous #The post is asynchronous due to the potencially long deploying time
	@engine
	def post(self):
		file1 = self.request.files['file'][0] #Only one file at a time

		original_fname = file1['filename']
		print(os.path.join(__UPLOADS__, original_fname))
		output_file = open(os.path.join(__UPLOADS__, original_fname), 'wb')
		output_file.write(file1['body'])
		output_file.close()
		
		# The nodes where to deploy are returned as a comma-separated string
		nodes = self.get_argument('nodes', '').split(',')[:-1] #TODO: no final comma
		from concurrent import futures
		
		#The deployment process is performed asynchronously using a ThreadPool, which will handle the request asynchronously
		thread_pool = futures.ThreadPoolExecutor(max_workers=len(nodes))
		
		#print("Print" + self.get_argument('overwrite', False));
		
		@tornado.gen.coroutine
		def call_deploy(node):
			yield thread_pool.submit(self.deploy, node=node,
			 request=self, filename=original_fname, 
			 command=self.get_argument('command', ''), 
			 user=self.current_user, 
			 folder=self.get_argument('folder',''),
			 tomcat=self.get_argument('tomcat', ''),
			 overwrite=self.get_argument('overwrite', 'false'))
		
		for node in nodes:
			future = self.deploy(node=node,
			 request=self, 
			 filename=original_fname, 
			 command=self.get_argument('command', ''), 
			 user=self.current_user, 
			 folder=self.get_argument('folder',''),
			 tomcat=self.get_argument('tomcat', ''),
			 overwrite=self.get_argument('overwrite', 'false'))


			#deployment = tornado.gen.Task(call_deploy, node)
		
		self.finish("file" + original_fname + " is uploaded and on deploy")
	
	@tornado.web.asynchronous
	def deploy(self, node, request, filename, command, user, folder="", idpolo="", tomcat="", overwrite='false'):
		
		def get_content_type(filename):
			return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

		url = "https://"+node+":"+str(conf.RECEIVER_PORT)+"/deploy"
		files = {'file': (filename, open(os.path.join(__UPLOADS__, filename), 'rb'), get_content_type(filename))}
		commands = {'command':command, 
					'user':user, 
					'folder': folder, 
					'idpolo': idpolo, 
					'tomcat': tomcat,
					'overwrite':overwrite
					}
		
		return futures_session.post(url, files=files, data=commands, verify=conf.RECEIVERCERT, cert=(conf.APPCERT, conf.APPKEY))
		
class NodesHandler(websocket.WebSocketHandler):
	"""
	Handler for the Polo websocket connection
	"""
	#TODO: polo will have events to notify of new nodes. New crazy idea...
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

class Nodes(RequestHandler):
	def get(self):
		m = marco.Marco()
		try:
			nodes = m.request_for("deployer")
			self.write(json.dumps({'nodes':[n.address[0] for n in nodes]}))
		except marco.MarcoTimeOutException:
			self.write_message(json.dumps({"Error": "Error in marco detection"}))
		

class ProbeHandler(RequestHandler):
	def get(self):
		self.write("You should be able to open a WebSocket connection right now")
		#TODO: Test the ws in the page

class ProbeWSHandler(websocket.WebSocketHandler):
	def check_origin(self, origin):
		return True

	def open(self):
		self.write_message("OK")
		self.close()
		
routes = [
	(r'/', IndexHandler),
	(r'/nodes', Nodes),
	(r'/static/(.*)', StaticFileHandler, {"path":"./static"}),
	(r'/ws/nodes', NodesHandler),
	(r"/login", LoginHandler),
    (r"/logout", Logout),
	(r'/upload', UploadAndDeployHandler),
	#probes
	(r'/probe', ProbeHandler),
	(r'/ws/probe', ProbeWSHandler)
]

settings = {
	"debug": True,
    "static_path": conf.STATIC_PATH,
    "login_url":"/login" , 
    "cookie_secret":"2a70b29a80c23f097a074626e584c8f60a87cf33f518f0eda60db0211c82"
}

app = Application(routes, **settings)

if __name__ == "__main__":
	
	pid = os.getpid()

	if not os.path.exists('/var/run/marcopolo'):
		makedirs('/var/run/marcopolo')

	f = open(conf.PIDFILE_DEPLOYER, 'w')
	f.write(str(pid))
	f.close()

	#TODO Replace with SSLContext (this option is maintained for compatibility reasons)
	httpServer = HTTPServer(app, ssl_options={ 
        "certfile": conf.APPCERT,
        "keyfile": conf.APPKEY,
    })

	httpServer.listen(conf.DEPLOYER_PORT)
	print("Serving on port %d" % conf.DEPLOYER_PORT)
	ioloop.IOLoop.instance().start()
	#TODO consider multicore server
