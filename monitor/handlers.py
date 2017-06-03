import os

from tornado import web, websocket
from tornado.template import Loader

import conf

class IndexHandler(web.RequestHandler):
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
            self.render(os.path.join(conf.TEMPLATES_DIR, 'index.html'))
            #self.redirect("/login/")
        else:
            self.render(os.path.join(conf.TEMPLATES_DIR, 'index.html'))
            #user = tornado.escape.xhtml_escape(self.current_user)
            #self.render("index.jade", user=user)

