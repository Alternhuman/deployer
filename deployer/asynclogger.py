from tornado.web import RequestHandler, Application, StaticFileHandler
from tornado import ioloop
from tornado.websocket import WebSocketHandler
import subprocess
import fcntl
import os
import sys

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
	def __init__(self, user, io_loop, opensockets, *args, **kwargs):
		self.user = user
		self.opensockets  =opensockets
		kwargs['stdout'] = subprocess.PIPE
		self.process = subprocess.Popen(*args, **kwargs)
		
		self.fd = self.process.stdout.fileno()
		fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
		fcntl.fcntl(self.fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

		io_loop.add_handler(self.process.stdout, self.can_read, io_loop.READ)

		self.line_buffer = LineBuffer()

	def can_read(self, fd, events):
		data = self.process.stdout.read(1024)
		if len(data) > 0:
			self.on_data(data)
		else:
			print("Lost connection to subprocess")
			sys.exit(1)

	def on_data(self, data):
		for line in self.line_buffer.read_lines(data):
			self.on_line(line.decode('utf-8'))

	def on_line(self, line):
		for ws in self.opensockets[self.user]:
			ws.on_line(self.user, line)


class ExecuteCommand():
	def __init__(self, user, ioloop, opensockets):
		self.user = user
		self.processreactor = ProcessReactor(user, ioloop, opensockets, ['cat', 'lines.txt'])