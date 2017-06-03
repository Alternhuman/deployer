import logging
import os
import signal
import sys
import json

import argparse

from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado import web, websocket, ioloop
from tornado.ioloop import PeriodicCallback

from statuscrawler import get_data
import conf
import handlers


io_loop = ioloop.IOLoop.instance()

callback_fn = None
data_dict = {}
data_json = ""
async def process_data():
    global data_dict, data_json
    data_dict = await get_data()
    data_json = json.dumps(data_dict)

open_ws = set()

def start_callback():
    """
    Starts the collection callback
    """
    global callback_fn
    if callback_fn is None:
        callback_fn = PeriodicCallback(process_data, conf.REFRESH_FREQUENCY)
        callback_fn.start()
    elif not callback_fn.is_running():
        callback_fn.start()

def stop_callback(force=False):
    """
    If the number of open connections is zero, stops the collection callback of data.
    """
    global callback_fn
    if callback_fn is not None:
        if force or len(open_ws) == 0:
            callback_fn.stop()

class WebSocketIndexHandler(websocket.WebSocketHandler):
    def open(self):
        open_ws.add(self)
        self.callback = PeriodicCallback(self.send_data, 1000)
        self.callback.start()
        start_callback()

    def send_data(self):
        self.write_message(data_json)

    def on_close(self):
        self.callback.stop()
        open_ws.remove(self)

def shutdown():
    #logging.info("Stopping gracefully")
    io_loop.stop()
    stop_callback()

def sigint_handler(signal, frame):
    io_loop.add_callback(shutdown)


routes = [
    (r'/', handlers.IndexHandler),
    (r'/ws/monitor/?', WebSocketIndexHandler),
]

if conf.DEBUG:
    routes += [
        (r'/static/(.*)', web.StaticFileHandler, {'path': conf.STATIC_PATH}),
    ]

signal.signal(signal.SIGINT, sigint_handler)

def main(args=None):

    parser = argparse.ArgumentParser(description='Monitoring utility')
    parser.add_argument('-p', '--port', type=int, help="Port where the application will listen to", default=conf.PORT)

    args = parser.parse_args()

    app = Application(routes, **conf.app_settings)
    http_server = HTTPServer(app)

    http_server.listen(args.port)
    start_callback()
    #logging.info("Serving on port %d" % conf.PORT)
    io_loop.start()

if __name__ == '__main__':
    main(sys.argv[1:])