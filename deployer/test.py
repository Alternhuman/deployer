import unittest
from tornado.web import Application
from  tornado.httpclient import HTTPRequest
from tornado.testing import AsyncTestCase
from tornado.httpclient import AsyncHTTPClient
import tornado
import sys, os
sys.path.append(os.path.dirname(__file__))
from os.path import dirname, join
from deployer import BaseHandler
import json
from tornado.httpclient import HTTPError
directory = dirname(__file__)
cert_dir = "certs"

certs = join(directory, cert_dir)

APPCERT = join(certs, "app.crt")
APPKEY  = join(certs, "app.key")

RECEIVERCERT = join(certs, "receiver.crt")
RECEIVERKEY = join(certs, "receiver.key")

#http://tornado.readthedocs.org/en/latest/testing.html
"""class TestAuthentication(unittest.TestCase):

	def setUp(self):
		self.auth = BaseHandler(Application(), HTTPRequest('/'))
		self.auth.set_secure_cookie("user", "martin")
	def test_user(self):
		self.assertFailure(self.auth.get_secure_cookie("user"), "martin")
"""
class TestIndex(AsyncTestCase):
	@tornado.testing.gen_test
	def test_http_fetch(self):
		client = AsyncHTTPClient(self.io_loop)
		response = yield client.fetch(HTTPRequest("https://localhost:1341/", 
			validate_cert=True, ca_certs=APPCERT))
		# Test contents of response
		self.assertEqual(200, response.code)

	def test_http_fail(self):
		client = AsyncHTTPClient(self.io_loop)
		client.fetch(HTTPRequest("https://localhost:1341/", method="POST",
			body="",
			validate_cert=True, ca_certs=APPCERT), self.handle_fetch)
		self.wait()
	
	def handle_fetch(self, response):
		self.assertEqual(405, response.code)
		self.stop()

class TestLogin(AsyncTestCase):
	@tornado.testing.gen_test
	def test_login(self):
		client = AsyncHTTPClient(self.io_loop)
		response = yield client.fetch(HTTPRequest("https://localhost:1341/login", method='POST',
			body="name=martin&pass=patata",
			validate_cert=True, ca_certs=APPCERT))
		
		self.assertEqual(200, response.code)

class TestLogout(AsyncTestCase):
	@tornado.testing.gen_test
	def test_logout(self):
		client = AsyncHTTPClient(self.io_loop)
		response = yield client.fetch(HTTPRequest("https://localhost:1341/logout", method='GET',
			validate_cert=True, ca_certs=APPCERT))
		
		self.assertEqual(200, response.code)

"""from unittest.mock import MagicMock
thing = ProductionClass()
thing.method = MagicMock(return_value=3)
thing.method(3, 4, 5, key='value')
#3
thing.method.assert_called_with(3, 4, 5, key='value')"""


"""
mock = Mock(side_effect=KeyError('foo'))
mock()
#Traceback (most recent call last):
# ...
#KeyError: 'foo'
"""


# This test uses argument passing between self.stop and self.wait.
class MyTestCase2(AsyncTestCase):
	def test_http_fetch(self):
		client = AsyncHTTPClient(self.io_loop)
		client.fetch("http://www.tornadoweb.org/", self.stop)
		response = self.wait()
		# Test contents of response
		self.assertIn(bytes("FriendFeed", 'utf-8'), response.body)

# This test uses an explicit callback-based style.
class MyTestCase3(AsyncTestCase):
	def test_http_fetch(self):
		client = AsyncHTTPClient(self.io_loop)
		client.fetch("http://www.tornadoweb.org/", self.handle_fetch)
		self.wait()

	def handle_fetch(self, response):
		# Test contents of response (failures and exceptions here
		# will cause self.wait() to throw an exception and end the
		# test).
		# Exceptions thrown here are magically propagated to
		# self.wait() in test_http_fetch() via stack_context.
		self.assertIn(bytes("FriendFeed", 'utf-8'), response.body)
		self.stop()


if __name__ == "__main__":
	unittest.main()




