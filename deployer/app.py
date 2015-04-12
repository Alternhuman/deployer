#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tornado.web import Application, RequestHandler, StaticFileHandler
import tornado.web
from tornado import web, websocket
from tornado import ioloop, template
from pyjade.ext.tornado import patch_tornado

import os, uuid
from io import StringIO
import random, string

patch_tornado()

import sys
sys.path.append('/home/martin/TFG/workspaces/discovery/marcopolo/')

from bindings.marco import marco
from marco_conf.utils import Node

import json

from tempfile import tempdir
import tempfile
__UPLOADS__ = tempfile.gettempdir()
__UPLOADS__ = "uploads/"

open_ws = set()

class IndexHandler(RequestHandler):
  """
  In charge of handling GET requests. Provides the client with the .html/css/js necessary
  """
  @web.addslash
  def get(self):
  	self.render("templates/index.jade")

class UploadAndDeployHandler(RequestHandler):
	"""
	Listens for POSTs requests and performs the deployment asynchronously
	"""
	@tornado.web.asynchronous#The post is asynchronous due to the potencially long deploying response time
	@tornado.gen.engine
	def post(self):
		file1 = self.request.files['file'][0] #Only one file at a time

		original_fname = file1['filename']
		output_file = open("uploads/" + original_fname, 'wb')
		output_file.write(file1['body'])
		nodes = self.get_argument('nodes', '').split(',')[:-1] # The nodes are returned as a comma-separated string
		
		from concurrent import futures
		
		#The deployment process is performed asynchronously using a ThreadPool, which will handle the request asynchronously
		thread_pool = futures.ThreadPoolExecutor(4)
		
		@tornado.gen.coroutine
		def call_blocking(node):
			yield thread_pool.submit(self.upload_to_the_net, node=node, request=self, filename=original_fname, command=self.get_argument('command', ''))
		
		for node in nodes:
			deployment = tornado.gen.Task(call_blocking, node)
		
		self.finish("file" + original_fname + " is uploaded and on deploy")
	
	@tornado.web.asynchronous
	def upload_to_the_net(self, node, request, filename, command):
		
		import requests, mimetypes
		def get_content_type (filename):
			return mimetypes.guess_type (filename)[0] or 'application/octet-stream'

		url = "http://"+node+":1339/deploy" #url ="http://localhost:1339/deploy"
		files = {'file': (filename, open("uploads/"+filename, 'rb'), get_content_type(filename))}
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

routes = [
	(r'/', IndexHandler),
	(r'/static/(.*)', StaticFileHandler, {"path":"./static"}),
	(r'/ws/nodes', NodesHandler),
	(r'/upload', UploadAndDeployHandler),
]

settings = {
	"debug": True,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
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