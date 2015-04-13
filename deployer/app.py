#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.web
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado import web, websocket, ioloop, template
from pyjade.ext.tornado import patch_tornado

import os
import random, string

patch_tornado()

import sys
sys.path.append('/opt/marcopolo/')

from bindings.marco import marco
from marco_conf.utils import Node

import json

from tempfile import tempdir
import tempfile

__UPLOADS__ = tempfile.gettempdir()

open_ws = set()
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class IndexHandler(BaseHandler):
	"""
	In charge of handling GET requests. Provides the client with the necessary .html/css/js
	"""
	@web.addslash
	def get(self):
		print(self.get_secure_cookie("user"))
		if not self.current_user:
			self.redirect("/login")
		else:
			user = tornado.escape.xhtml_escape(self.current_user)
			self.render("templates/index.jade", user=user)
			#self.render("templates/index.jade", logged=True, user="patata")



class LoginHandler(BaseHandler):
	def get(self):
		if self.current_user:
			self.redirect("/")
		else:
			self.render("templates/login.jade")

	def post(self):
		if authenticate(self.get_argument("name"), self.get_argument("pass")):
			self.set_secure_cookie("user", self.get_argument("name"))

		self.redirect("/")

class Logout(BaseHandler):
	def get(self):
		self.clear_cookie("user")
		self.redirect("/")

class UploadAndDeployHandler(RequestHandler):
	"""
	Listens for POSTs requests and performs the deployment asynchronously
	"""
	@tornado.web.asynchronous #The post is asynchronous due to the potencially long deploying response time
	@tornado.gen.engine
	def post(self):
		file1 = self.request.files['file'][0] #Only one file at a time

		original_fname = file1['filename']
		output_file = open(os.path.join(__UPLOADS__, original_fname), 'wb')
		output_file.write(file1['body'])
		
		# The nodes are returned as a comma-separated string
		nodes = self.get_argument('nodes', '').split(',')[:-1] 
		from concurrent import futures
		
		#The deployment process is performed asynchronously using a ThreadPool, which will handle the request asynchronously
		thread_pool = futures.ThreadPoolExecutor(max_workers=len(nodes))
		
		@tornado.gen.coroutine
		def call_deploy(node):
			yield thread_pool.submit(self.deploy, node=node, request=self, filename=original_fname, command=self.get_argument('command', ''))
		
		for node in nodes:
			deployment = tornado.gen.Task(call_deploy, node)
		
		self.finish("file" + original_fname + " is uploaded and on deploy")
	
	@tornado.web.asynchronous
	def deploy(self, node, request, filename, command):
		
		import requests, mimetypes
		def get_content_type(filename):
			return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

		url = "http://"+node+":1339/deploy"
		files = {'file': (filename, open(os.path.join(__UPLOADS__, filename), 'rb'), get_content_type(filename))}
		commands = {'command': command}
		r = requests.post(url, files=files, data=commands)
		

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
			nodes = m.request_for("statusmonitor")
			self.write_message(json.dumps({"Nodes":[n.address[0] for n in nodes]}))
		except marco.MarcoTimeOutException:
			self.write_message(json.dumps({"Error": "Error in marco detection"}))
		 		
	def send_data(self):
		pass

	def on_close(self):
		pass

	def send_update(self):
		pass


from os import path
from crypt import crypt
from re import compile as compile_regex

#http://code.activestate.com/recipes/578489-system-authentication-against-etcshadow-or-etcpass/
def authenticate(name, password):
	"""
	Returns true or false depending on the success of the name-password combination using
	the shadows or passwd file (The shadow file is preferred if it exists) 
	"""
	
	if path.exists("/etc/shadow"):
		import spwd
		shadow = spwd.getspnam(name).sp_pwdp # https://docs.python.org/3.4/library/spwd.html#module-spwd
	else:
		import pwd
		shadow = pwd.getpwnam(name).pw_passwd
	
	salt_pattern = compile_regex(r"\$.*\$.*\$")
	
	salt = salt_pattern.match(shadow).group()
	
	return crypt(password, salt) == shadow


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
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "login_url":"/" , 
    "cookie_secret":"2a70b29a80c23f097a074626e584c8f60a87cf33f518f0eda60db0211c82"
}

app = Application(routes, **settings)

if __name__ == "__main__":
	app.listen(8080)
	ioloop.IOLoop.instance().start()

	"""Multicore:def main():
	app = make_app()
	server = tornado.httpserver.HTTPServer(app)
	server.bind(8888)
	server.start(0)  # forks one process per cpu
	IOLoop.current().start()"""