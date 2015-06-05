#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado
from tornado.web import Application, RequestHandler, \
StaticFileHandler, asynchronous
from tornado import web, websocket, ioloop
from tornado.httpserver import HTTPServer
from tornado.gen import engine

import os, json, mimetypes, conf



import sys, signal
from os import makedirs


from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession
from pyjade.ext.tornado import patch_tornado
patch_tornado() #Allows pyjade to work with Tornado

sys.path.append('/opt/marcopolo/') #Temporary fix to append the path

from bindings.marco import marco
from bindings.polo import polo
#from marco_conf.utils import Node
import utils

# TODOimport random, string, tempfile
# from tornado import template
# from tempfile import tempdir
# import ssl
# from os import path
# import requests


class NotCheckingHostnameHTTPAdapter(HTTPAdapter):
    """
    A middleware that avoids the verification of the SSL Hostname field.
    Since the name of the client cannot be verified,
    it is simply not checked
    
    From Juan Luis Boya
    """
    def cert_verify(self, conn, *args, **kwargs):
        """
        Avoids the verification of the SSL Hostname field

        :param: conn The connection object
        """
        super().cert_verify(conn, *args, **kwargs)
        conn.assert_hostname = False

# By changing the adapter no hostname is checked
futures_session = FuturesSession()
futures_session.mount('https://', NotCheckingHostnameHTTPAdapter())

#Creation of the temporal directory if it does not exists
if not os.path.exists(conf.TMPDIR):
    os.makedirs(conf.TMPDIR)

__UPLOADS__ = conf.TMPDIR # temporal directory were files will be stored

open_ws = set() #Set of the current alive websockets

class BaseHandler(RequestHandler):
    """
    The base class which the rest of HTTP handlers extends.
    Provides secure cookie decryption and error handling
    """
    def get_current_user(self):
        """
        Decrypts the secure cookie

        :return: The name of the user or None
        :rtype: string
        """
        return self.get_secure_cookie("user")

    def write_error(self, status_code, **kwargs):
        self.render("templates/500.jade")


class IndexHandler(BaseHandler):
    """
    In charge of handling GET requests.
    Provides the client with the necessary .html/css/js
    """
    @web.addslash #Appends a '/' at the end of the request
    def get(self):
        """
        Checks if the user is logged and sends the index files
        (basic HTML, CSS and JS).
        If the user is not already logged in, it is redirected 
        to the main page. 
        """
        if not self.current_user:
            self.redirect("/login/")
        else:
            user = tornado.escape.xhtml_escape(self.current_user)
            self.render("templates/index.jade", user=user)

class LoginHandler(BaseHandler):
    """
    Handles login authentication through secure cookies and PAM
    """
    def get(self):
        """
        Returns the login page if the user is not logged.
        Otherwise redirects to the index site.
        """
        if self.current_user:
            self.redirect("/")
        else:
            self.render("templates/login.jade")

    def post(self):
        """
        Processes login requests using PAM. If the user and password combination
        is valid, the response is given a secure cookie, and the user gets 
        redirected to the new index site.
        Otherwise, a 403 page is returned.
        """
        if utils.authenticate(self.get_argument("name"), 
                              self.get_argument("pass")):

            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect("/")
        else:
            self.set_status(403)
            self.render("templates/badpass.jade")

class Logout(BaseHandler):
    """
    Removes the secure cookie.
    """
    def get(self):
        """
        Removes the secure cookie and redirects the user to the index folder.
        """
        self.clear_cookie("user")
        self.redirect("/")

class UploadAndDeployHandler(BaseHandler):
    """
    Listens for POST requests and performs the deployment asynchronously.
    """
    #The post is asynchronous due to the potencially long deploying time
    @asynchronous
    @engine
    def post(self):
        """
        Receives a set of parameters through an asynchronous POST request:

        - file : A binary stream of data which corresponds to a file uploaded by the user.

        - folder : The folder where the file has to be stored

        - tomcat : Specifies that the service is a Tomcat container and that it must be added to the offered services

        - overwrite : If true, the file will overwrite a previous file with the same name

        - command : A command to execute when after the deployment

        - nodes : The nodes where the file and command are to be deployed

        Writes a status code to the client in return
        """
        file1 = self.request.files['file'][0] #Only one file at a time

        original_fname = file1['filename']
        #print(os.path.join(__UPLOADS__, original_fname))
        output_file = open(os.path.join(__UPLOADS__, original_fname), 'wb')
        output_file.write(file1['body'])
        output_file.close()
        
        # The nodes where to deploy are returned as a comma-separated string
        nodes = self.get_argument('nodes', '').split(',')[:-1] #TODO: no final comma
        from concurrent import futures
        
        """The deployment process is performed asynchronously 
        using a ThreadPool, which will handle the request asynchronously"""
        #TODO: remove?
        #thread_pool = futures.ThreadPoolExecutor(max_workers=len(nodes))

        #For each node a future is received

        futures_set = set()

        for node in nodes:
            future = self.deploy(node=node,
             request=self, 
             filename=original_fname, 
             command=self.get_argument('command', ''), 
             user=self.current_user, 
             folder=self.get_argument('folder', ''), 
             tomcat=self.get_argument('tomcat', ''), 
             overwrite=self.get_argument('overwrite', 'false'))
            
            futures_set.add((future, node))

        error = []
       
        for future, node in futures_set:
            try:
                response = future.result()
                
                if response.status_code > 400:
                    error.append((node, response.reason))
            except Exception as e:
                error.append((node, "Could not connect to the node"))

        if len(error) > 0:
            self.finish("Errors occurred " + 
                " ".join(["Node:"+node+"." for node, reason in error]))
        else:
            self.finish("file" + original_fname + " is uploaded and on deploy")
    
    def deploy(self, node, request, filename, command, user, folder="", idpolo="", tomcat="", overwrite='false'):
        """
        Performs the deployment asynchronously.

        :param: :class:`str` The IP address of the node
        :param: :class:`BaseHandler` The related POST request which invoked this method *Deprecated*
        :param: str filename The name of the file to upload
        :param: str command The command to execute after deployment
        :param: str user The name of the user who performs the request
        :param: str folder The deployment folder
        :param: str idpolo The id of the polo service to publish
        :param: str tomcat Specifies whether the file should be deployed as a tomcat service
        :param: str overwrite Specifies if the file can overwrite existing files

        :returns: :class:`concurrent.future` A future that encapsulates the asynchronous execution 
        """
        def get_content_type(filename):
            """
            Guesses the MIME type of the file so it can be sent with the POST request

            :param: str filename The name of the file to process
            """
            return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

        url = "https://"+node+":"+str(conf.RECEIVER_PORT)+"/deploy/"
        
        files = {'file': (filename, 
                    open(os.path.join(__UPLOADS__, filename), 'rb'), 
                    get_content_type(filename))
                }
        
        commands = {'command':command, 
                    'user':user, 
                    'folder': folder, 
                    'idpolo': idpolo, 
                    'tomcat': tomcat,
                    'overwrite':overwrite
                    }
        
        try:
            f = futures_session.post(url, files=files, data=commands, verify=conf.RECEIVERCERT, cert=(conf.APPCERT, conf.APPKEY))
        
            return f
        except Exception as e:
            print("It happened here")

class NodesHandler(websocket.WebSocketHandler):
    """
    Handler for the Polo websocket connection
    """
    def check_origin(self, origin):
        """
        Overrides the parent method to return True for any request, since we are
        working without names. 

        :see: :meth:`check_origin<tornado.websocket.WebSocketHandler.check_origin>`

        :returns: bool True
        """
        return True

    def open(self):
        """
        Processes a new WebSocket connection, storing it in open_ws.
        Returns the nodes offering the deployer service
        """
        open_ws.add(self)
        m = marco.Marco()
        try:
            nodes = m.request_for("deployer")
            self.write_message(json.dumps({"Nodes":[n.address for n in nodes]}))
        except marco.MarcoTimeOutException:
            self.write_message(json.dumps({"Error": "Error in marco detection"}))
                
    def send_data(self):
        pass

    def on_close(self):
        pass

    def send_update(self):
        pass

class Nodes(RequestHandler):
    """
    Performs a synchronous Marco request for the deployer service
    """
    #TODO: Make async
    def get(self):
        """
        Returns a JSON string with the nodes offering the deployer service
        """
        m = marco.Marco()
        try:
            nodes = m.request_for("deployer")
            self.write(json.dumps({'nodes':[n.address for n in nodes]}))
        except marco.MarcoTimeOutException:
            self.write_message(json.dumps({"Error": "Error in marco detection"}))
        

class ProbeHandler(RequestHandler):
    """
    A test connection to trigger the web browser certificate validation,
    since WebSockets cannot request user confirmation by themselves.
    """
    def get(self):
        self.write("You should be able to open a WebSocket connection right now")
        #TODO: Test the ws in the page

class ProbeWSHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        """
        Overrides the parent method to return True for any request, since we are
        working without names

        :see: :meth:`check_origin<tornado.websocket.WebSocketHandler.check_origin>`

        :returns: bool True
        """

        #:ref:`Tornado documentation: <tornado:WebSocketHandler.check_origin>`
        return True

    def open(self):
        self.write_message("OK")
        self.close()


routes = [
    (r'/', IndexHandler),
    (r'/nodes/?', Nodes),
    (r'/static/(.*)', StaticFileHandler, {"path":"./static"}),
    (r'/ws/nodes/?', NodesHandler),
    (r"/login/?", LoginHandler),
    (r"/logout/?", Logout),
    (r'/upload/?', UploadAndDeployHandler),
    #probes
    (r'/probe/?', ProbeHandler),
    (r'/ws/probe/?', ProbeWSHandler)
]

settings = {
    "debug": True,
    "static_path": conf.STATIC_PATH,
    "login_url":"/login/",
    "cookie_secret":"2a70b29a80c23f097a074626e584c8f60a87cf33f518f0eda60db0211c82"
}

app = Application(routes, **settings)
io_loop = ioloop.IOLoop.instance()


def shutdown():
    print("Stopping gracefully")
    try:
        polo.Polo().unpublish_service(conf.RECEIVER_SERVICE_NAME, delete_file=True)
        polo.Polo().unpublish_service(conf.STATUS_MONITOR_SERVICE_NAME, delete_file=True)
    except Exception as e:
        print(e)
    io_loop.stop()

def sigint_handler(signal, frame):
    io_loop.add_callback(shutdown)

signal.signal(signal.SIGINT, sigint_handler)

if __name__ == "__main__":
    
    

    
    pid = os.getpid()

    if not os.path.exists('/var/run/marcopolo'):
        makedirs('/var/run/marcopolo')

    f = open(conf.PIDFILE_DEPLOYER, 'w')
    f.write(str(pid))
    f.close()

    #TODO Replace with SSLContext (this option is maintained for compatibility reasons)
    httpServer = HTTPServer(app, ssl_options={ 
        "certfile": conf.APPCERT,
        "keyfile": conf.APPKEY,
    })

    httpServer.listen(conf.DEPLOYER_PORT)

    while True:
        try:
            polo.Polo().publish_service(conf.DEPLOYER_SERVICE_NAME, root=True)
            break
        except polo.PoloInternalException as e:
            print(e)
            time.sleep(1)
        except polo.PoloException as i:
            print(i)
            break

    print("Serving on port %d" % conf.DEPLOYER_PORT)
    io_loop.start()
    #TODO consider multicore server
