#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tornado.web import Application, RequestHandler
import tornado.web
from tornado import ioloop
import os

class DeployHandler(RequestHandler):
	def post(self):
		file1 = self.request.files['file'][0]
		
		original_fname = file1['filename']
		output_file = open("/home/martin/Desktop/" + original_fname, 'wb')
		output_file.write(file1['body'])
		print("The command is: " + self.get_argument('command', ''))
		self.write('OK')

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