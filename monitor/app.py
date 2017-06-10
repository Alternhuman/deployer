import argparse
import json
import logging
import os
import signal
import sys

from tornado import ioloop, web, websocket
from tornado.httpserver import HTTPServer
from tornado.ioloop import PeriodicCallback
from tornado.web import Application

import conf
import handlers
from statuscrawler import get_data

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
        if force or not open_ws:
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

def sigint_handler(*args):
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
