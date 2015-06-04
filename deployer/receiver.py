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

from bufferprocessor import ProcessReactor

if int(sys.version[0]) < 3:
	import urlparse
else:
	import urllib.parse as urlparse

ip = ""
opensockets={}
io_loop = ioloop.IOLoop.instance()
data_dict = {}
data_json = ""

response_dict = {}
statusmonitor_open_sockets =  []
getDataCallback = None
processes = set()

from utils import getip 

def sigterm_handler(signal, frame):
    ioloop.IOLoop.instance().stop()
    for socket in statusmonitor_open_sockets:
        socket.close()
    sys.exit(0)

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
		if len(command) > 0:
			p = ProcessReactor(user, directory, io_loop, ip, opensockets, split(command))
			processes.add(p)
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
		#global ip
		#ip = getip(conf.INTERFACE)
		pass
	def on_message(self, message):
		"""
		A message is sent by the client after creating the connection. The method verifies the user
		secret cookie and appends the connection to the opensockets dictionary.
		"""
		user_id = decode_signed_value(settings["cookie_secret"], 'user', json.loads(message).get("register", "")).decode('utf-8')
		
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

	def on_line(self, user, command, message, ip, identifier, stop=False, stream_name="stdout", *args, **kwargs):
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
		msg["stop"] = stop
		msg["stream_name"] = stream_name
		msg["shell"] = kwargs.get("shell", False)
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

class ShellHandler(LoggerHandler):
	
	def on_message(self, message):
		message_json = message.decode('utf-8')

		try:
			message_dict = json.loads(message_json)
		except ValueError as v:
			return

		if message_dict.get("register", None) is not None:
			user_id = decode_signed_value(settings["cookie_secret"], 'user', message_dict["register"]).decode('utf-8')
			
			if not user_id is None:
				if opensockets.get(user_id) is None:
					opensockets[user_id] = []#TODO: change to set
				opensockets[user_id].append(self)
			else:
				pass

		elif message_dict.get("command", None) is not None:
			user_id = decode_signed_value(settings["cookie_secret"], 'user', message_dict.get("user_id", ""))
			

			if user_id is not None:
				user_id = user_id.decode('utf-8')
				user_pwd = pwd.getpwnam(user_id)
				try:
					command = message_dict["command"]
					p = ProcessReactor(user_pwd, user_pwd.pw_dir, io_loop, ip, opensockets, split(command), shell=True)
					processes.add(p)
				except Exception as e:
					print(e)

		elif message_dict.get("remove", None) is not None:
			print("remove")
			user_id = decode_signed_value(settings["cookie_secret"], 'user', message_dict.get("user_id", ""))
			if user_id is not None:
				identifier = message_dict.get("remove", None)
				if identifier is not None:
					print("identifier", identifier)
					process = next((x for x in processes if x.identifier == identifier), None)
					if process is not None:
						process.stop()

		elif message_dict.get("removeshell", None) is None:
			user_id = decode_signed_value(settings["cookie_secret"], 'user', message_dict.get("user_id", ""))
			if user_id is not None:
				
				identifiers = message_dict.get("removeshell")
				if identifiers is not None:
					try:
						identifiers_dict = json.loads(message_dict["removeshell"])
						for identifier in identifiers:
							process = next((x for x in processes if x.identifier == identifier), None)
							if process is not None:
								process.stop()
					except ValueError as v:
						print(v)


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


def start_callback():
	global getDataCallback
	if getDataCallback is None:
		getDataCallback = PeriodicCallback(process_data, conf.REFRESH_FREQ)  
		getDataCallback.start()
	elif not getDataCallback.is_running():
		getDataCallback.start()

def stop_callback():
	global getDataCallback
	if getDataCallback is not None:
		if len(statusmonitor_open_sockets) == 0:
			getDataCallback.stop()

def process_data():
	"""
	
	"""
	global data_dict, data_json
	if len(statusmonitor_open_sockets) > 0:
		data_dict = get_data()
		data_json = json.dumps(data_dict,separators=(',',':'))


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
        if not self in statusmonitor_open_sockets:
            statusmonitor_open_sockets.append(self) #http://stackoverflow.com/a/19571205
        self.callback = PeriodicCallback(self.send_data, 1000)

        self.callback.start()
        start_callback()

    def send_data(self):
        self.write_message(data_json)
        return

        
    def on_close(self):
        self.callback.stop()
        if self in statusmonitor_open_sockets:
            statusmonitor_open_sockets.remove(self)

        stop_callback()

    def send_update(self):
        pass



routes =  [
	(r'/deploy/?', DeployHandler),
]

routes_ws = [
	(r'/ws/probe/', ProbeWSHandler),
	(r'/ws/status/', SocketHandler),
	(r'/ws/logger/', ShellHandler),
	(r'/probe/', ProbeHandler),
	(r'/', ProbeHandler),
]

app = Application(routes, **settings)

wsapp = Application(routes_ws, **settings);


if __name__ == "__main__":
	ip = getip(conf.INTERFACE)
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

	#getDataCallback = PeriodicCallback(process_data, conf.REFRESH_FREQ)  
	#getDataCallback.start()

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
