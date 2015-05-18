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
from tornado.gen import coroutine
import sys
sys.path.append(os.path.realpath(__file__))
import conf

import signal
from os import path, makedirs

class DeployHandler(RequestHandler):
	@tornado.web.asynchronous
	def post(self):
		"""
		POST handler received from deployer.py. 
		It handles the deployment of the file and the execution of the desired command.
		"""

		file1 = self.request.files['file'][0]
		
		command = self.get_argument('command', '')
		idpolo = self.get_argument('idpolo', '')
		tomcat = self.get_argument('tomcat', '')
		
		if not tomcat:
			folder = self.get_argument('folder', '')
		else:
			folder = conf.TOMCAT_PATH

		fname = file1['filename']
		
		user = self.get_argument('user', '')
		
		user_pwd = pwd.getpwnam(user)
		
		#Handling of relative paths
		folder = folder.replace('~', user_pwd.pw_dir, 1)
		
		if len(folder) == 0 or folder[0] != '/':
			folder = os.path.join(user_pwd.pw_dir, folder)

		if folder == '':
			folder = user_pwd.pw_dir


		final_directory = os.path.join(folder, fname)
		print(final_directory)
		
		overwrite = self.get_argument('overwrite', 'false')
		print(overwrite)
		overwrite = False if overwrite.lower() == 'false' else True;

		print("Overwrite: " + str(overwrite))
		from concurrent import futures

		@coroutine
		def call_execute():
			yield thread_pool.submit(self.execute, command=command, file_desc=file1, filename=final_directory, directory=folder, user=user_pwd, tomcat=tomcat, overwrite=overwrite)
			
		thread_pool = futures.ThreadPoolExecutor(max_workers=4)
		thread_pool.submit(self.execute, command=command, file_desc=file1, filename=final_directory, directory=folder, user=user_pwd, tomcat=tomcat, overwrite=overwrite)
		
		self.finish('OK')

	@tornado.web.asynchronous
	def execute(self, command, file_desc, filename, directory, user, tomcat=False, overwrite="false"):
		
		if os.path.isfile(filename) and not overwrite:
			print("File already exists and cannot overwrite")
			return
		else:
			print("Overwriting all the things!")
		def demote(user_uid, user_gid):
			os.setgid(user_gid)
			os.setuid(user_uid)
			
		if os.path.exists(os.path.dirname(filename)):
			output_file = open(filename, 'wb')
		else:
			print("Path does not exist")
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

from asynclogger import ExecuteCommand
from tornado.websocket import WebSocketHandler

opensockets={}
settings = {
	"debug": True,
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
	"cookie_secret": "2a70b29a80c23f097a074626e584c8f60a87cf33f518f0eda60db0211c82"
}

class LoggerHandler(WebSocketHandler):
	def check_origin(self, origin):
		return True
	
	def open(self):
		self.write_message("Hola")

	def on_message(self, message):
		from tornado.web import decode_signed_value
		user_id = decode_signed_value(settings["cookie_secret"], 'user', message)
		if not user_id is None:
			if opensockets.get(user_id) is None:
				opensockets[user_id] = []
			opensockets[user_id].append(self)

	def on_close(self):
		success = False
		for ws in opensockets:
			if self in opensockets[ws]:
				opensockets[ws].remove(self)

routes =  [
	(r'/deploy', DeployHandler),
]


app = Application(routes, **settings)
class IndexHandler2(RequestHandler):
	def get(self):
		self.write("HOla")

wsapp = Application([(r'/', IndexHandler2),(r'/ws/', LoggerHandler)], **settings);

if __name__ == "__main__":
	import conf, ssl

	pid = os.getpid()

	if not os.path.exists('/var/run/deployer'):
		makedirs('/var/run/deployer')

	f = open(conf.PIDFILE_RECEIVER, 'w')
	f.write(str(pid))
	f.close()

	httpServer = HTTPServer(app, ssl_options={
		"certfile": conf.RECEIVERCERT,
		"keyfile": conf.RECEIVERKEY,
		"cert_reqs": ssl.CERT_OPTIONAL,
		"ca_certs": conf.APPCERT,
		})

	httpServer.listen(conf.RECEIVER_PORT)

	wsapp.listen(1370, ssl_options={"certfile": conf.APPCERT,
        "keyfile": conf.APPKEY})

	print("Starting receiver on port %d" % conf.RECEIVER_PORT)
	ioloop.IOLoop.instance().start()
