#!/usr/bin/env python3

import tornado.web
import shadowauth
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado import web, websocket, ioloop, template

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   'Pass: <input type="text" name="pass">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        if shadowauth.authenticate(self.get_argument("name"), self.get_argument("pass")):
            import random
            self.set_secure_cookie("user", self.get_argument("name"))
        
        self.redirect("/")

class Logout(BaseHandler):
	def get(self):
		self.clear_cookie("user")
		self.redirect("/")

class Require(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.write("yay!")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/logout", Logout),
    (r"/require", Require),
], login_url="/login" , cookie_secret="2a70b29a80c23f097a074626e584c8f60a87cf33f518f0eda60db0211c82")

if __name__ == "__main__":
	application.listen(9000)
	ioloop.IOLoop.instance().start()