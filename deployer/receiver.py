#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado import ioloop
from tornado.websocket import WebSocketHandler
import tornado.web
from tornado.httpserver import HTTPServer 
from tornado import ioloop
from tornado.gen import coroutine

import os, time
from shlex import split
from subprocess import Popen
import subprocess
import pwd
import sys


sys.path.append(os.path.realpath(__file__))
import conf
from statusmonitor import get_data
from tornado.ioloop import PeriodicCallback
import signal
from os import path, makedirs

import subprocess
import fcntl
import sys
import json

import socket
import string, random
import hashlib
from concurrent import futures
from tornado.web import decode_signed_value
import logging
import conf, ssl


sys.path.append("/opt/marcopolo")
from bindings.polo import polo

from netifaces import AF_INET
import netifaces as ni
if int(sys.version[0]) < 3:
	import urlparse
else:
	import urllib.parse as urlparse

ip = ""



def getip(protocol=None, host=None):
	"""
	Returns the IP associated with the configured interface
	"""
	return ni.ifaddresses(conf.INTERFACE).get(AF_INET)[0].get('addr')

def sigint_handler(signal, frame):
	io_loop.add_callback(shutdown)

def shutdown():
	print("Stopping gracefully")
	try:
		polo.Polo().unpublish_service("deployer", delete_file=True)
		polo.Polo().unpublish_service("statusmonitor", delete_file=True)
	except Exception as e:
		print(e)
	io_loop.stop()

signal.signal(signal.SIGINT, sigint_handler)

opensockets={}

io_loop = ioloop.IOLoop.instance()

class LineBuffer(object):
	"""
	Processes each linke in the desired buffer

	From Juan Luis Boya
	"""
	def __init__(self):
		self.buffer = b''

	def read_lines(self, input):
		"""
		Processes each line and appends it to the buffer
		"""
		while b'\n' in input:
			before, after = input.split(b'\n', 1)
			yield self.buffer + before
			self.buffer = b''
			input = after
		self.buffer += input

class ProcessReactor(object):
	def __init__(self, user, directory, *args, **kwargs):
		"""
		Starts the command and sets the redirection of the desired buffers
		:param: :class:pwd user The pwd structure with the information of the user which issued the command
		:param: str directory The directory to use as cwd
		:param: :class:list args A list of supplementary arguments
		:param: :class:dict kwargs A dictionary of keyword arguments

		The function redirects STDOUT and STDERR to a pipe, and then executes the command using Popen.
		The output pipe descriptor is made non-blocking and included in the instance of the IOLoop. 
		"""

		self.user = user #user which executes the command
		self.command = ' '.join(*args) # The name of the command
		self.ip = ip # The IP of the server

		def randomString():
			"""
			Generates a random token

			:returns: A random string which acts as a token
			"""
			return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(3))

		# Generates a random token to identify the execution
		self.identifier = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
		
		self.opensockets  = opensockets
		
		#The buffers are redirected
		kwargs['stdout'] = subprocess.PIPE
		kwargs['stderr'] = subprocess.PIPE
		
		def demote(uid, gid):
			"""
			The UID and GID of the child process is changed to match those of the user
			who issued the command. Otherwise the operation would be executed as root.
			"""
			os.setgid(gid)
			os.setuid(uid)


		self.process = subprocess.Popen(preexec_fn=demote(user.pw_uid, user.pw_gid), #function executed before the call
										cwd=directory, # The current working directory is changed
										*args, **kwargs)
		
		#The fileno of the stdout buffer is used to make it non-blocking
		self.fd = self.process.stdout.fileno()
		fl = fcntl.fcntl(self.fd, fcntl.F_GETFL) #The file access mode is returned
		fcntl.fcntl(self.fd, fcntl.F_SETFL, fl | os.O_NONBLOCK) # The flags of the file are modified, appending the non-blocking flag blogin

		#The same for stderr
		self.fd_err = self.process.stderr.fileno()
		fl_err = fcntl.fcntl(self.fd_err, fcntl.F_GETFL)
		fcntl.fcntl(self.fd_err, fcntl.F_SETFL, fl | os.O_NONBLOCK)

		#Creation of the line buffer
		self.line_buffer = LineBuffer()

		#Two handlers are registered, each for one of the output buffers. can_read and can_read_stderr act as the callback for events related to both of them
		io_loop.add_handler(self.process.stdout, self.can_read, io_loop.READ)
		io_loop.add_handler(self.process.stderr, self.can_read_stderr, io_loop.READ)
		

	def can_read(self, fd, events):
		"""
		Processes the stdout event
		:param: int fd The file descriptor of the stdout buffer
		:param: int events The event flags (bitwise OR of the constants IOLoop.READ, IOLoop.WRITE, and IOLoop.ERROR)
		"""
		data = self.process.stdout.read(1024)
		

		if len(data) > 0:
			"""If the length of the data is larger than zero, the information is sent to all
			the listening sockets"""
			self.on_data(data, "stdout")

		else:
			print("Lost connection to subprocess")
			io_loop.remove_handler(self.process.stdout)
			self.stop_output()
	
	def can_read_stderr(self, fd, events):
		"""
		Processes the stderr event
		:param: int fd The file descriptor of the stderr buffer
		:param: int events The event flags (bitwise OR of the constants IOLoop.READ, IOLoop.WRITE, and IOLoop.ERROR)
		"""
		data = self.process.stderr.read(1024)

		if len(data) > 0:
			self.on_data(data, "stderr")

		else:
			print("Lost connection to subprocess")
			io_loop.remove_handler(self.process.stderr)
			self.stop_output()

	def on_data(self, data, stream_name):
		"""
		Decodes the data and passes it to on_line
		:param: byte[] data an array of bytes with the message
		:param: str stream_name The name of the stream
		"""
		for line in self.line_buffer.read_lines(data):
			self.on_line(line.decode('utf-8'), stream_name)

	def on_line(self, line, stream_name):
		"""
		Sends the line to the open websocket
		:param: str line The message line
		:param: str stream_name The name of the stream
		"""
		for ws in self.opensockets[self.user.pw_name]:
			ws.on_line(self.user.pw_name, self.command, line, self.ip, self.identifier, False, stream_name)


	def stop_output(self):
		"""
		Sends a special message to close the websocket connection
		"""
		for ws in self.opensockets[self.user.pw_name]:
			ws.on_line(self.user.pw_name, self.command, None, self.ip, self.identifier, True)

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

		if not os.path.isdir(folder):
			return

		if not os.path.exists(folder):
			makedirs(folder)
			chown(folder, user.pw_uid, user.pw_gid)


		final_directory = os.path.join(folder, fname)
		
		overwrite = self.get_argument('overwrite', 'false')
		
		overwrite = False if overwrite.lower() == 'false' else True;


		thread_pool = futures.ThreadPoolExecutor(max_workers=4) #TODO
		thread_pool.submit(self.execute, command=command, file_desc=file1, filename=final_directory, directory=folder, user=user_pwd, tomcat=tomcat, overwrite=overwrite)
		
		self.finish('OK')

	@tornado.web.asynchronous
	def execute(self, command, file_desc, filename, directory, user, tomcat=False, overwrite="false"):
		
		if os.path.isfile(filename) and not overwrite:
			return

		def demote(user_uid, user_gid):
			os.setgid(user_gid)
			os.setuid(user_uid)
			
		if os.path.exists(os.path.dirname(filename)):
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
			p = ProcessReactor(user, directory, split(command))
			#TODOprocess = Popen(split(command), preexec_fn=demote(user.pw_uid, user.pw_gid), cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			#TODOout, err = process.communicate()


settings = {
	"debug": True,
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
	"cookie_secret": "2a70b29a80c23f097a074626e584c8f60a87cf33f518f0eda60db0211c82"
}

class LoggerHandler(WebSocketHandler):
	"""
	Processes the logging messages
	"""
	def check_origin(self, origin):
		"""
        Overrides the parent method to return True for any request, since we are
        working without names

        :ref:`Tornado documentation: <tornado:WebSocketHandler.check_origin>`
        :returns: bool True
        """
		return True
	
	def open(self):
		#TODO: remove
		global ip
		ip = getip(self.request.protocol, self.request.host)

	def on_message(self, message):
		"""
		A message is sent by the client after creating the connection. The method verifies the user
		secret cookie and appends the connection to the opensockets dictionary.
		"""
		user_id = decode_signed_value(settings["cookie_secret"], 'user', message).decode('utf-8')
		
		"""
		If the user_id is other than None the verification has succeded, and the connection is appended to the 
		rest of the websockets related to the user.
		"""
		if not user_id is None:
			if opensockets.get(user_id) is None:
				opensockets[user_id] = []#TODO: change to set
			opensockets[user_id].append(self)
		else:
			pass
		#TODO: Return error code

	def on_line(self, user, command, message, ip, identifier, stop=False, stream_name="stdout"):
		"""
		The io_loop calls the function when a new message appears.
		:param: str user The name of the user
		:param: str command The command in execution
		:param: str message The message to deliver
		:param: str ip The ip of the server, so the client knows where the message comes from
		:param: bool stop Determines if the connection must be closed or not *deprecated*
		:param: str stream_name The name of the stream
		"""
		#TODO Could the client side of the ws guess the address
		#TODO: Remove stop
		msg = {}
		msg["user"] = user
		msg["command"] = command
		msg["message"] = message
		msg["ip"] = ip
		msg["identifier"] = identifier
		msg["stop"] = False
		msg["stream_name"] = stream_name
		
		self.write_message(json.dumps(msg))

	def on_close(self):
		"""
		Removes the connection from the opensockets dictionary
		"""
		success = False
		for ws in opensockets:
			if self in opensockets[ws]:
				opensockets[ws].remove(self)
				success = True
				break #TODO:  Remove success

class ProbeWSHandler(WebSocketHandler):
	def check_origin(self, origin):
		"""
        Overrides the parent method to return True for any request, since we are
        working without names

        :ref:`Tornado documentation: <tornado:WebSocketHandler.check_origin>`
        :returns: bool True
        """
		return True

	def open(self):
		"""
		Returns a confirmation message
		"""
		self.write_message("OK")
		self.close()


class ProbeHandler(RequestHandler):
	def get(self):
		self.write("You should be able to create websocket connections now")


def process_data():
	"""
	
	"""
	global data_dict, data_json

	data_dict = get_data()
	data_json = json.dumps(data_dict,separators=(',',':'))

data_dict = {}
data_json = ""

response_dict = {}
open_sockets =  []
class SocketHandler(WebSocketHandler):

    def check_origin(self, origin):
    	"""
        Overrides the parent method to return True for any request, since we are
        working without names

        :ref:`Tornado documentation: <tornado:WebSocketHandler.check_origin>`
        :returns: bool True
        """
        return True

    def open(self):
        print("Connection open from " + self.request.remote_ip)
        if not self in open_sockets:
            open_sockets.append(self) #http://stackoverflow.com/a/19571205
        self.callback = PeriodicCallback(self.send_data, 1000)

        self.callback.start()

    def send_data(self):
        self.write_message(data_json)
        return

        
    def on_close(self):
        self.callback.stop()
        if self in open_sockets:
            open_sockets.remove(self)

    def send_update(self):
        pass



routes =  [
	(r'/deploy/?', DeployHandler),
]

routes_ws = [
	(r'/ws/probe/', ProbeWSHandler),
	(r'/ws/status/', SocketHandler),
	(r'/ws/logger/', LoggerHandler),
	(r'/probe/', ProbeHandler),
	(r'/', ProbeHandler),
]

app = Application(routes, **settings)

wsapp = Application(routes_ws, **settings);

if __name__ == "__main__":
	ip = getip()
	pid = os.getpid()

	if not os.path.exists('/var/run/marcopolo'):
		makedirs('/var/run/marcopolo')

	f = open(conf.PIDFILE_RECEIVER, 'w')
	f.write(str(pid))
	f.close()

	httpServer = HTTPServer(app, ssl_options={
		"certfile": conf.RECEIVERCERT,
		"keyfile": conf.RECEIVERKEY,
		"cert_reqs": ssl.CERT_REQUIRED,
		"ca_certs": conf.APPCERT,
	})

	httpServer.listen(conf.RECEIVER_PORT)

	wsapp.listen(conf.RECEIVER_WEBSOCKET_PORT, 
			ssl_options={"certfile": conf.APPCERT,
	        			 "keyfile": conf.APPKEY})

	getDataCallback = PeriodicCallback(process_data, conf.REFRESH_FREQ)  
	getDataCallback.start()

	while True:
		try:
			polo.Polo().publish_service("deployer", root=True)
			polo.Polo().publish_service("statusmonitor", root=True)
			break
		except polo.PoloInternalException as e:
			print(e)
			time.sleep(1)
		except polo.PoloException as i:
			print(i)
			break
	print("Starting receiver on port %d. WebSockets on %d" % (conf.RECEIVER_PORT, conf.RECEIVER_WEBSOCKET_PORT))
	io_loop.start()
