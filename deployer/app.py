from tornado.web import Application, RequestHandler, StaticFileHandler
import tornado.web
from tornado import web, websocket
from tornado import ioloop, template
from pyjade.ext.tornado import patch_tornado

patch_tornado()


class IndexHandler(RequestHandler):
  @web.addslash
  def get(self):
  	self.render("templates/index.jade")

  #def initialize(self, db) Example for magic, then in url, dict(db=db)

class NodesHandler(websocket.WebSocketHandler):
	#polo will have events to notify of new nodes. New crazy idea...
	def check_origin(self):
		return True

	def open(self):
		pass # call polo

	def send_data(self):
		pass

	def on_close(self):
		pass

	def send_update(self):
		pass

routes = [
	(r'/', IndexHandler),
	(r'/static/(.*)', StaticFileHandler, {"path":"./static"}),
	(r'/ws/nodes', NodesHandler),
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