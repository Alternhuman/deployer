#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

__author__ = 'Diego Martín'

from tornado import web, websocket, ioloop
from tornado.ioloop import PeriodicCallback
from time import time, gmtime, strftime, localtime
import subprocess, signal, sys, os
import json

import conf

PORT = 1341
response_dict = {}
open_sockets =  []

def sigterm_handler(signal, frame):
    ioloop.IOLoop.instance().stop()
    for socket in open_sockets:
        socket.close()
    sys.exit(0)

def get_data():

        global response_dict

        response_dict["time"] = strftime("%a, %d %b %Y %H:%M:%S", localtime())

        response_dict["hostname"] = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        response_dict["ip"] = subprocess.Popen("/sbin/ifconfig eth0| grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        if len(response_dict["ip"]) == 0:
            response_dict["ip"] = subprocess.Popen(" /sbin/ifconfig eth0 | grep 'inet\ ' | cut -d: -f2 | awk '{ print $2 }'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

        response_dict["uptime"] = subprocess.Popen("uptime | tail -n 1 | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        response_dict["kernel_name"] = subprocess.Popen("uname -r", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        response_dict["top"] = subprocess.Popen("top -d 0.5 -b -n2 | tail -n 10 | awk '{print $12}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

        response_dict["memtotal"] = subprocess.Popen("egrep --color 'MemTotal' /proc/meminfo | egrep '[0-9.]{4,}' -o",
                        shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

        response_dict["memfree"] = subprocess.Popen("egrep --color 'MemFree' /proc/meminfo | egrep '[0-9.]{4,}' -o", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        response_dict["membuffered"] = subprocess.Popen("egrep --color 'Buffers' /proc/meminfo | egrep '[0-9.]{4,}' -o", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        response_dict["memcached"] = subprocess.Popen("egrep --color 'Cached' /proc/meminfo | egrep '[0-9.]{4,}' -o", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

        response_dict["swaptotal"] = subprocess.Popen("egrep --color 'SwapTotal' /proc/meminfo | egrep '[0-9.]{4,}' -o", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        response_dict["swapfree"] = subprocess.Popen("egrep --color 'SwapFree' /proc/meminfo | egrep '[0-9.]{4,}' -o", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

        response_dict["temperature"] = float(subprocess.Popen("cat /sys/class/thermal/thermal_zone0/temp", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')) / 1000.0
        response_dict["top"] = subprocess.Popen("top -d 0.5 -b -n2 | grep 'Cpu(s)'|tail -n 1 | awk '{print $2 + $4}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        response_dict["uptime"] = subprocess.Popen("uptime | tail -n 1 | awk '{print $3 $4 $5}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        response_dict["top_list"] = subprocess.Popen("ps aux --width 30 --sort -rss --no-headers | head  | awk '{print $11}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

        #cpus = subprocess.Popen("mpstat -P ALL | grep -A 5 "+'"%idle"'+ "| tail -n +3 | awk -F"+' " "'+" '{print $ 12 }'",shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').split('\n')
        cpus = subprocess.Popen("top -d 0.4 -b -n2 | grep \"Cpu\" | tail -n 4 | awk '{print $2 + $4}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').split('\n')

        try:
            cpus.remove("")
        except ValueError:
            pass
        #subprocess.Popen("top -b -n1 | grep Cpu | sed -r 's@.+:\s([0-9\.]+).+@\1@' | awk '{ print $4 }' | grep \"[0-9]\"|cut -f 1 -d '['", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').split('\n')
        cpus_float = [float(c.replace(',','.')) for c in cpus]
        
        response_dict["cpus"] = cpus_float

class SocketHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print("Connection open from " + self.request.remote_ip)
        if not self in open_sockets:
            open_sockets.append(self) #http://stackoverflow.com/a/19571205
        self.callback = PeriodicCallback(self.send_data, 1000)

        self.callback.start()

    def send_data(self):

        global response_dict
        chain = json.dumps(response_dict,separators=(',',':'))

        self.write_message(chain)

        return

        
    def on_close(self):
        self.callback.stop()
        if self in open_sockets:
            open_sockets.remove(self)

    def send_update(self):
        pass

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

class ProbeHandler(web.RequestHandler):
    def get(self):
        self.write("OK")

class ProbeSocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message("OK")
        self.close()

app = web.Application([
    (r'/probe', ProbeHandler),
    (r'/ws/probe/', ProbeSocketHandler),
    (r'/ws', SocketHandler),
], **settings)

if __name__ == "__main__":
    import signal, os, logging
    signal.signal(signal.SIGHUP, signal.SIG_IGN)

    pid = os.getpid()
    
    if not os.path.exists('/var/run/marcopolo'):
        os.makedirs('/var/run/marcopolo')
    
    f = open("/var/run/marcopolo/statusmonitor.pid", 'w')
    f.write(str(pid))
    f.close()

    getDataCallback = PeriodicCallback(get_data, 1000)  
    getDataCallback.start()
    
    signal.signal(signal.SIGINT, sigterm_handler)
    from tornado.httpserver import HTTPServer
    
    httpServer = HTTPServer(app, ssl_options={ 
        "certfile": conf.APPCERT,
        "keyfile": conf.APPKEY,
    })

    httpServer.listen(PORT)
    print("Starting application on port %d" % PORT)
    ioloop.IOLoop.instance().start()
