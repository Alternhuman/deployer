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
		fname = file1['filename']
		
		if folder == "":
			folder = "/home/martin/Desktop/"
		
		final_directory = os.path.join(folder, fname)
		output_file = open(final_directory, 'wb')
		output_file.write(file1['body'])
		output_file.close()

		from concurrent import futures

		@tornado.gen.coroutine
		def call_execute():
			yield thread_pool.submit(self.execute, command=command, filename=final_directory, directory=folder)
			
		thread_pool = futures.ThreadPoolExecutor(max_workers=1)
		tornado.gen.Task(call_execute)

		self.finish('OK')

	@tornado.web.asynchronous
	def execute(self, command, filename, directory):
		Popen(split(command), cwd=directory)


		"""import requests, mimetypes
		def get_content_type(filename):
			return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

		url = "http://"+node+":1339/deploy"
		files = {'file': (filename, open(os.path.join(__UPLOADS__, filename), 'rb'), get_content_type(filename))}
		commands = {'command': command}
		r = requests.post(url, files=files, data=commands)"""

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
