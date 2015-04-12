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

open_ws = set()

class IndexHandler(RequestHandler):
  @web.addslash
  def get(self):
  	#self.set_cookie("id", "aaa", domain=None, path="/*", expires_days=1)
  	self.render("templates/index.jade")

  #def initialize(self, db) Example for magic, then in url, dict(db=db)

class UploadAndDeployHandler(RequestHandler):
	@tornado.web.asynchronous
	@tornado.gen.engine
	def post(self):
		file1 = self.request.files['file'][0]
		#print("Command: " + self.get_argument('command', ''))
		#print("Nodes: " + self.get_argument('nodes', ''))

		#
		#print(nodes)
		original_fname = file1['filename']
		final_filename = original_fname
		output_file = open("uploads/" + final_filename, 'wb')
		output_file.write(file1['body'])
		nodes = self.get_argument('nodes', '').split(',')[:-1]
		
		from concurrent import futures
		
		thread_pool = futures.ThreadPoolExecutor(4)
		
		#print(self.request.body)

		@tornado.gen.coroutine
		def call_blocking():
			#yield thread_pool.submit(self.upload_to_nodes, request=self, nodes=nodes, files=self.request.files['file'][0])
			#yield thread_pool.submit(self.upload_to_minions, request=self, filedata=file1)
			yield thread_pool.submit(self.upload_to_the_net, request=self, filename=final_filename, command=self.get_argument('command', ''))
		
		deployment = tornado.gen.Task(call_blocking)
		
	@tornado.web.asynchronous
	def upload_to_the_net(self, request, filename, command):
		import requests, mimetypes
		def get_content_type (filename):
			return mimetypes.guess_type (filename)[0] or 'application/octet-stream'

		url ="http://localhost:1339/deploy"
		files = {'file': (filename, open("uploads/"+filename, 'rb'), get_content_type(filename))}
		commands = {'command': command}
		r = requests.post(url, files=files, data=commands)
		#print(r)
		request.finish("file" + "Patata" + " is uploaded")

	@tornado.web.asynchronous
	def upload_to_minions(self, request, filedata):
		lista_fields = []
		lista_fields.append(["command", request.get_argument('command', '')])

		lista_files = []
		#lista_files.append(["file", files])
		lista_files.append(filedata)
		
		print("\n\n\nLe form:\n\n\n")
		
		body, headers = self.create_new_body(lista_fields, lista_files)
		print(body)
		request.finish("file" + "Patata" + " is uploaded")
		"""url ="http://localhost:8080/send_file"
		import urllib.request
		import http.client
		req = urllib.request.Request (url)
		connection = http.client.HTTPConnection (req.host)
		connection.request ('POST', req.selector, body, headers)
		response = connection.getresponse ()
		print(response)
		request.finish("file" + "Patata" + " is uploaded")
		return"""

	def create_new_body(self, lista_fields, lista_files):
		import mimetypes
		
		boundary = '----------ThIs_Is_tHe_bouNdaRY_$'

		def get_content_type (filename):
			return mimetypes.guess_type (filename)[0] or 'application/octet-stream'

		def encode_field (field_name, field_value):
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"' % field_name,
				'', str (field_value))

		def encode_file(field_name, filename, content_type, file_data):
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
				'Content-Type: %s' % content_type,
				'', file_data)


		def encode_file2 (field_name):
			filename = files [field_name]
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
				'Content-Type: %s' % get_content_type(filename),
				'', open (filename, 'rb').read ())

		def encode_file3 (filevar):
			filename = filevar ['filename']
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"; filename="%s"' % ('file', filename),
				'Content-Type: %s' % get_content_type(filename),
				'', open ("uploads/" + filename, 'rb').read ())

		lines = []
		for (name, value) in lista_fields:
			lines.extend (encode_field (name, value))
		for name in lista_files:
			lines.extend (encode_file3 (name))
		
		#lines.extend()
		lines.extend (('--%s--' % boundary, ''))
		#ba = bytes(lines, 'ascii')
		bb = bytes('\r\n', 'ascii')
		bb.join(lines);
		#body = bytes('\r\n', 'ascii').join(bytes(lines, 'ascii'))
		#body = lines
		print(body)
		headers = {'content-type': 'multipart/form-data; boundary=' + boundary,
		          'content-length': str (len (body))}

		return body, headers

	#@tornado.web.asynchronous
	def create_body(self, fields, files):
		import string, random
		BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
		#BOUNDARY = ''.join (random.choice (string.letters) for ii in range (30 + 1))
		CRLF = '\r\n'
		L = []
		for (key, value) in fields:
			L.append('--' + BOUNDARY)
			L.append('Content-Disposition: form-data; name="%s"' % key)
			L.append('')
			L.append(value)
		for(key, value) in files:
			filename = value['filename']
			L.append('--' + BOUNDARY)
			L.append(
				'Content-Disposition: form-data; name="%s"; filename="%s"' % (
					key, filename
				)
			)
			L.append('Content-Type: %s' % value['content_type'])
			L.append('')
			L.append(value['body'])
			L.append('--' + BOUNDARY + '--')
			L.append('')

		body = CRLF.join(L)
		headers = {'content-type': 'multipart/form-data; boundary=' + BOUNDARY,
               'content-length': str (len (body))}

		return body, headers
	def encode_multipart_data (data, files):
		boundary = random_string (30)

		def get_content_type (filename):
			return mimetypes.guess_type (filename)[0] or 'application/octet-stream'

		def encode_field (field_name):
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"' % field_name,
				'', str (data [field_name]))

		def encode_file(field_name, filename, content_type, file_data):
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
				'Content-Type: %s' % content_type,
				'', file_data)


		def encode_file2 (field_name):
			filename = files [field_name]
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
				'Content-Type: %s' % get_content_type(filename),
				'', open (filename, 'rb').read ())

		lines = []
		for name in data:
			lines.extend (encode_field (name))
		#for name in files:
		#	lines.extend (encode_file (name))
		
		lines.extend()
		lines.extend (('--%s--' % boundary, ''))
		body = '\r\n'.join (lines)

		headers = {'content-type': 'multipart/form-data; boundary=' + boundary,
		          'content-length': str (len (body))}

		return body, headers

	@tornado.web.asynchronous
	def upload_to_nodes(self, request, nodes, files=None, fields=None, callback=None, raise_error=True, **kwargs):
		
		lista_fields = []
		lista_fields.append(["command", request.get_argument('command', '')])

		lista_files = []
		lista_files.append(["file", files])
		#lista_files.append(["file", request.files['file'][0]])
		
		print("\n\n\nLe form:\n\n\n")
		
		body, headers = self.create_body(lista_fields, lista_files)
		url ="http://localhost:8080/send_file"
		import urllib.request
		import http.client
		req = urllib.request.Request (url)
		connection = http.client.HTTPConnection (req.host)
		connection.request ('POST', req.selector, body, headers)
		response = connection.getresponse ()
		print(response)
		request.finish("file" + "Patata" + " is uploaded")
		return

		#http://stackoverflow.com/a/28613273/2628463
		import mimetypes
		def encode_multipart_formdata(fields, files):
			"""
			fields is a sequence of (name, value) elements for regular form fields.
			files is a sequence of (name, filename, value) elements for data to be
			uploaded as files.
			Return (content_type, body) ready for httplib.HTTP instance
			"""
			BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
			CRLF = '\r\n'
			L = []
			"""for (key, value) in fields:
				L.append('--' + BOUNDARY)
				L.append('Content-Disposition: form-data; name="%s"' % key)
				L.append('')
				L.append(value)"""
			for (key, filename, value) in files:
				filename = filename.encode("utf8")
				L.append('--' + BOUNDARY)
				L.append(
					'Content-Disposition: form-data; name="%s"; filename="%s"' % (
						key, filename
					)
				)
				L.append('Content-Type: %s' % get_content_type(filename))
				L.append('')
				L.append(value)
			L.append('--' + BOUNDARY + '--')
			L.append('')
			body = CRLF.join(L)
			content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
			return content_type, body


		def get_content_type(filename):
			try:
				return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
			except TypeError:
				return 'application/octet-stream'
		content_type, body = encode_multipart_formdata(fields, files)
		#headers = {"Content-Type": content_type, 'content-length': str(len(body))}
		#request = HTTPRequest(url, "POST", headers=headers, body=body, validate_cert=False)
		print(content_type)
		print(body)
		import time
		time.sleep(10)
		print("End sleep")
		request.finish("file" + "Patata" + " is uploaded")
		#callback()

class NodesHandler(websocket.WebSocketHandler):
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

class UploadFile(RequestHandler):
	def post(self):

		print(self.request.files['file'][0])
		
		file1 = self.request.files['file'][0]
		original_fname = file1['filename']
		final_filename = original_fname
		print(original_fname)
		output_file = open("/home/martin/Desktop/" + final_filename, 'wb')
		#print(type(file1['body']))
		output_file.write(file1['body'])
		self.write('OK')

routes = [
	(r'/', IndexHandler),
	(r'/static/(.*)', StaticFileHandler, {"path":"./static"}),
	(r'/ws/nodes', NodesHandler),
	(r'/upload', UploadAndDeployHandler),
	(r'/send_file', UploadFile),
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