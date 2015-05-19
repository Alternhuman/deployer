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

from tornado.web import RequestHandler, Application, StaticFileHandler
from tornado import ioloop
from tornado.websocket import WebSocketHandler
import subprocess
import fcntl
import os
import sys
#from asynclogger import ExecuteCommand
from tornado.websocket import WebSocketHandler
import json

import socket
import string, random
import hashlib

if int(sys.version[0]) < 3:
	import urlparse
else:
	import urllib.parse as urlparse
ip = ""
def getip(protocol, host):
	print(host)
	hostname = urlparse.urlparse("%s://%s" % (protocol, host)).hostname
	ip_address = socket.gethostbyname(hostname)
	return "172.20.1.88"
	return ip_address

opensockets={}

io_loop = ioloop.IOLoop.instance()

class LineBuffer(object):
	def __init__(self):
		self.buffer = b''

	def read_lines(self, input):
		while b'\n' in input:
			before, after = input.split(b'\n', 1)
			yield self.buffer + before
			self.buffer = b''
			input = after
		self.buffer += input

class ProcessReactor(object):
	def __init__(self, user, directory, *args, **kwargs):
		self.user = user
		self.command = ' '.join(*args)
		self.ip = ip
		def randomString():

			return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(3))

		#self.identifier = "AAA"#int(hashlib.sha1(self.command+randomString()).hexdigest(), 16) % (10 ** 8)
		self.identifier = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
		self.opensockets  = opensockets
		kwargs['stdout'] = subprocess.PIPE
		kwargs['stderr'] = subprocess.PIPE
		#print(args)
		def demote(uid, gid):
			os.setgid(gid)
			os.setuid(uid)

		self.process = subprocess.Popen(preexec_fn=demote(user.pw_uid, user.pw_gid), cwd=directory, *args, **kwargs)
		
		self.fd = self.process.stdout.fileno()
		fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
		fcntl.fcntl(self.fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

		self.fd_err = self.process.stderr.fileno()
		fl_err = fcntl.fcntl(self.fd_err, fcntl.F_GETFL)
		fcntl.fcntl(self.fd_err, fcntl.F_SETFL, fl | os.O_NONBLOCK)

		self.line_buffer = LineBuffer()
		io_loop.add_handler(self.process.stdout, self.can_read, io_loop.READ)
		io_loop.add_handler(self.process.stderr, self.can_read_stderr, io_loop.READ)
		

	def can_read(self, fd, events):
		data = self.process.stdout.read(1024)
		
		if len(data) > 0:
			self.on_data(data, "stdout")

		else:
			print("Lost connection to subprocess")
			io_loop.remove_handler(self.process.stdout)
			self.stop_output()
	def can_read_stderr(self, fd, events):
		data = self.process.stderr.read(1024)

		if len(data) > 0:
			self.on_data(data, "stderr")

		else:
			print("Lost connection to subprocess")
			io_loop.remove_handler(self.process.stderr)
			self.stop_output()

	def on_data(self, data, stream_name):
		#print(data)
		for line in self.line_buffer.read_lines(data):
			#print(line.decode('utf-8'))
			self.on_line(line.decode('utf-8'), stream_name)

	def on_line(self, line, stream_name):
		#print(self.user.pw_name)
		for ws in self.opensockets[self.user.pw_name]:
			ws.on_line(self.user.pw_name, self.command, line, self.ip, self.identifier, False, stream_name)

	def stop_output(self):
		for ws in self.opensockets[self.user.pw_name]:
			ws.on_line(self.user.pw_name, self.command, None, self.ip, self.identifier, True)


# class ExecuteCommand():
# 	def __init__(self, user, ioloop, opensockets):
# 		self.user = user.pw_name
# 		self.processreactor = ProcessReactor(user, ioloop, opensockets, ['cat', 'lines.txt'])

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
		#print(final_directory)
		
		overwrite = self.get_argument('overwrite', 'false')
		#print(overwrite)
		overwrite = False if overwrite.lower() == 'false' else True;

		#print("Overwrite: " + str(overwrite))
		from concurrent import futures

		thread_pool = futures.ThreadPoolExecutor(max_workers=4)
		thread_pool.submit(self.execute, command=command, file_desc=file1, filename=final_directory, directory=folder, user=user_pwd, tomcat=tomcat, overwrite=overwrite)
		
		self.finish('OK')

	@tornado.web.asynchronous
	def execute(self, command, file_desc, filename, directory, user, tomcat=False, overwrite="false"):
		
		if os.path.isfile(filename) and not overwrite:
			#print("File already exists and cannot overwrite")
			return
		else:
			#print("Overwriting all the things!")
			pass
		def demote(user_uid, user_gid):
			os.setgid(user_gid)
			os.setuid(user_uid)
			
		if os.path.exists(os.path.dirname(filename)):
			output_file = open(filename, 'wb')
		else:
			#print("Path does not exist")
			return

		output_file.write(file_desc['body'])
		if not tomcat:
			os.chown(filename, user.pw_uid, user.pw_gid)
		else:
			os.chown(filename, pwd.getpwnam('tomcat7').pw_uid, pwd.getpwnam('tomcat7').pw_gid)
		output_file.close()
		if command is not "":
			p = ProcessReactor(user, directory, split(command))
			#process = Popen(split(command), preexec_fn=demote(user.pw_uid, user.pw_gid), cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			#out, err = process.communicate()


settings = {
	"debug": True,
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
	"cookie_secret": "2a70b29a80c23f097a074626e584c8f60a87cf33f518f0eda60db0211c82"
}

class LoggerHandler(WebSocketHandler):
	def check_origin(self, origin):
		return True
	
	def open(self):
		global ip
		ip = getip(self.request.protocol, self.request.host)

	def on_message(self, message):
		from tornado.web import decode_signed_value
		user_id = decode_signed_value(settings["cookie_secret"], 'user', message).decode('utf-8')
		#print(user_id)
		if not user_id is None:
			if opensockets.get(user_id) is None:
				opensockets[user_id] = []
			opensockets[user_id].append(self)
			print("Opening socket")

	def on_line(self, user, command, message, ip, identifier, stop=False, stream_name="stdout"):
		#print("on_line")
		#print (message)
		if stop:
			print("stopping")
			msg={}
			msg["user"] = user
			msg["ip"] = ip
			msg["command"] = command
			msg["identifier"] = identifier
			msg["stop"] = True
			msg["stream_name"] = stream_name
			
		else:
			msg = {}
			msg["user"] = user
			msg["command"] = command
			msg["message"] = message
			msg["ip"] = ip
			msg["identifier"] = identifier
			msg["stop"] = False
			msg["stream_name"] = stream_name
		#print(msg)
		self.write_message(json.dumps(msg))

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
		self.write("Hola")

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

	#print("Starting receiver on port %d" % conf.RECEIVER_PORT)
	
	io_loop.start()
