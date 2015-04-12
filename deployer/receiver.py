#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tornado.web import Application, RequestHandler
import tornado.web
from tornado import ioloop
import os
from shlex import split
from subprocess import Popen
class DeployHandler(RequestHandler):
	@tornado.web.asynchronous
	def post(self):
		file1 = self.request.files['file'][0]
		
		
		command = self.get_argument('command', '')
		folder = self.get_argument('folder', '')
		original_fname = file1['filename']
		
		if folder == ""
			folder = "/home/martin/Desktop/"
		
		output_file = open(folder + original_fname, 'wb')
		output_file.write(file1['body'])
		
		#Popen(shlex.split(command), cwd=)
		self.finish('OK')

routes =  [(
	r'/deploy', DeployHandler
	)]

settings = {
	"debug": True,
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
}
app = Application(routes, **settings)

if __name__ == "__main__":
	app.listen(1339)
	ioloop.IOLoop.instance().start()