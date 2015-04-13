#!/usr/bin/env python3
# -*- coding: utf-8

import requests, os
from requests.adapters import HTTPAdapter
current_dir = os.path.dirname(__file__)
certdir = os.path.join(current_dir, "certs")

class NotCheckingHostnameHTTPAdapter(HTTPAdapter):
	def cert_verify(self, conn, *args, **kwargs):
		super().cert_verify(conn, *args, **kwargs)
		conn.assert_hostname = False

websession = requests.session()
websession.mount('https://', NotCheckingHostnameHTTPAdapter())

payload = {'key1': 'Hola', 'key2': 'value2'}
r = websession.post("https://localhost:9001/", data=payload, 
	verify=os.path.join(certdir, "receiver.crt"), 
		cert=(os.path.join(certdir, "app.crt"), os.path.join(certdir, "app.key")))

"""#!/usr/bin/env python3
# -*- coding: utf-8

import requests, os
from requests.adapters import HTTPAdapter
current_dir = os.path.dirname(__file__)
certdir = os.path.join(current_dir, "certs")

class NotCheckingHostnameHTTPAdapter(HTTPAdapter):
	def cert_verify(self, conn, *args, **kwargs):
		super().cert_verify(conn, *args, **kwargs)
		conn.assert_hostname = False

websession = requests.session()
websession.mount('https://', NotCheckingHostnameHTTPAdapter())

payload = {'key1': 'Hola', 'key2': 'value2'}
r = websession.post("https://localhost:9001/", data=payload, 
	verify=os.path.join(certdir, "minion.pem"), 
		cert=(os.path.join(certdir, "malote.pem"), os.path.join(certdir, "malote.key")))"""