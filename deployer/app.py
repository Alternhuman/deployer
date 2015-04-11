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

__UPLOADS__ = "uploads/"

class IndexHandler(RequestHandler):
  @web.addslash
  def get(self):
  	self.render("templates/index.jade")

  #def initialize(self, db) Example for magic, then in url, dict(db=db)

class UploadAndDeployHandler(RequestHandler):
	def post(self):
		file1 = self.request.files['file'][0]
		print("Command: " + self.get_argument('command', ''))
		original_fname = file1['filename']
		extension = os.path.splitext(original_fname)[1]
		fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
		final_filename= fname+extension
		output_file = open("uploads/" + final_filename, 'wb')
		output_file.write(file1['body'])
		self.finish("file" + final_filename + " is uploaded")

class NodesHandler(websocket.WebSocketHandler):
	#polo will have events to notify of new nodes. New crazy idea...
	def check_origin(self, origin):
		return True

	def open(self):
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
	(r'/upload', UploadAndDeployHandler)
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