#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tornado.web import Application, RequestHandler
import tornado.web
from tornado.httpserver import HTTPServer 
from tornado import ioloop
import os
from shlex import split
from subprocess import Popen
import subprocess
import pwd

import sys
sys.path.append(os.path.realpath(__file__))
import conf

class DeployHandler(RequestHandler):
	@tornado.web.asynchronous
	def post(self):
		file1 = self.request.files['file'][0]
		
		command = self.get_argument('command', '')
		idpolo = self.get_argument('idpolo', '')
		tomcat = self.get_argument('tomcat', False)
		
		if not tomcat:
			folder = self.get_argument('folder', '')
		else:
			folder = conf.TOMCAT_PATH
		fname = file1['filename']
		
		user = self.get_argument('user', '')
		
		user_pwd = pwd.getpwnam(user)
		
		if folder == '':
			folder = user_pwd.pw_dir
				
		#deployment_folder = os.path.join(user_home, folder)

		final_directory = os.path.join(folder, fname)

		
		from concurrent import futures

		@tornado.gen.coroutine
		def call_execute():
			yield thread_pool.submit(self.execute, command=command, file_desc=file1, filename=final_directory, directory=folder, user=user_pwd, tomcat=tomcat)
			
		thread_pool = futures.ThreadPoolExecutor(max_workers=1)
		tornado.gen.Task(call_execute)

		self.finish('OK')

	@tornado.web.asynchronous
	def execute(self, command, file_desc, filename, directory, user, tomcat=False):
		
		def demote(user_uid, user_gid):
			os.setgid(user_gid)
			os.setuid(user_uid)

		if os.path.exists(os.dirname(filename)):
			output_file = open(filename, 'wb')
		else:
			return
		output_file.write(file_desc['body'])
		if not tomcat:
			os.chown(filename, user.pw_uid, user.pw_gid)
		else:
			os.chown(filename, pwd.getpwnam('tomcat7').pw_uid, pwd.getpwnam('tomcat7').pw_gid)
		output_file.close()
		if command is not "":
			process = Popen(split(command), preexec_fn=demote(user.pw_uid, user.pw_gid), cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = process.communicate()
			print(out)
			print(err)

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
	import conf, ssl

	httpServer = HTTPServer(app, ssl_options={
		"certfile": conf.RECEIVERCERT,
		"keyfile": conf.RECEIVERKEY,
		"ssl_version": ssl.CERT_OPTIONAL,
		"cert_reqs": ssl.CERT_OPTIONAL,
		"ca_certs": conf.APPCERT,
		})
	httpServer.listen(conf.RECEIVER_PORT)
	ioloop.IOLoop.instance().start()
