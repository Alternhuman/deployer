@tornado.web.asynchronous
	def upload_to_minions(self, request, filedata):
		lista_fields = []
		lista_fields.append(["command", request.get_argument('command', '')])

		lista_files = []
		#lista_files.append(["file", files])
		lista_files.append(filedata)
		
		print("\n\n\nLe form:\n\n\n")
		
		body, headers = self.create_new_body(lista_fields, lista_files)
		print(body)
		request.finish("file" + "Patata" + " is uploaded")
		"""url ="http://localhost:8080/send_file"
		import urllib.request
		import http.client
		req = urllib.request.Request (url)
		connection = http.client.HTTPConnection (req.host)
		connection.request ('POST', req.selector, body, headers)
		response = connection.getresponse ()
		print(response)
		request.finish("file" + "Patata" + " is uploaded")
		return"""

	def create_new_body(self, lista_fields, lista_files):
		import mimetypes
		
		boundary = '----------ThIs_Is_tHe_bouNdaRY_$'

		def get_content_type (filename):
			return mimetypes.guess_type (filename)[0] or 'application/octet-stream'

		def encode_field (field_name, field_value):
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"' % field_name,
				'', str (field_value))

		def encode_file(field_name, filename, content_type, file_data):
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
				'Content-Type: %s' % content_type,
				'', file_data)


		def encode_file2 (field_name):
			filename = files [field_name]
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
				'Content-Type: %s' % get_content_type(filename),
				'', open (filename, 'rb').read ())

		def encode_file3 (filevar):
			filename = filevar ['filename']
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"; filename="%s"' % ('file', filename),
				'Content-Type: %s' % get_content_type(filename),
				'', open ("uploads/" + filename, 'rb').read ())

		lines = []
		for (name, value) in lista_fields:
			lines.extend (encode_field (name, value))
		for name in lista_files:
			lines.extend (encode_file3 (name))
		
		#lines.extend()
		lines.extend (('--%s--' % boundary, ''))
		#ba = bytes(lines, 'ascii')
		bb = bytes('\r\n', 'ascii')
		bb.join(lines);
		#body = bytes('\r\n', 'ascii').join(bytes(lines, 'ascii'))
		#body = lines
		print(body)
		headers = {'content-type': 'multipart/form-data; boundary=' + boundary,
		          'content-length': str (len (body))}

		return body, headers

	#@tornado.web.asynchronous
	def create_body(self, fields, files):
		import string, random
		BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
		#BOUNDARY = ''.join (random.choice (string.letters) for ii in range (30 + 1))
		CRLF = '\r\n'
		L = []
		for (key, value) in fields:
			L.append('--' + BOUNDARY)
			L.append('Content-Disposition: form-data; name="%s"' % key)
			L.append('')
			L.append(value)
		for(key, value) in files:
			filename = value['filename']
			L.append('--' + BOUNDARY)
			L.append(
				'Content-Disposition: form-data; name="%s"; filename="%s"' % (
					key, filename
				)
			)
			L.append('Content-Type: %s' % value['content_type'])
			L.append('')
			L.append(value['body'])
			L.append('--' + BOUNDARY + '--')
			L.append('')

		body = CRLF.join(L)
		headers = {'content-type': 'multipart/form-data; boundary=' + BOUNDARY,
               'content-length': str (len (body))}

		return body, headers
	def encode_multipart_data (data, files):
		boundary = random_string (30)

		def get_content_type (filename):
			return mimetypes.guess_type (filename)[0] or 'application/octet-stream'

		def encode_field (field_name):
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"' % field_name,
				'', str (data [field_name]))

		def encode_file(field_name, filename, content_type, file_data):
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
				'Content-Type: %s' % content_type,
				'', file_data)


		def encode_file2 (field_name):
			filename = files [field_name]
			return ('--' + boundary,
				'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
				'Content-Type: %s' % get_content_type(filename),
				'', open (filename, 'rb').read ())

		lines = []
		for name in data:
			lines.extend (encode_field (name))
		#for name in files:
		#	lines.extend (encode_file (name))
		
		lines.extend()
		lines.extend (('--%s--' % boundary, ''))
		body = '\r\n'.join (lines)

		headers = {'content-type': 'multipart/form-data; boundary=' + boundary,
		          'content-length': str (len (body))}

		return body, headers

	@tornado.web.asynchronous
	def upload_to_nodes(self, request, nodes, files=None, fields=None, callback=None, raise_error=True, **kwargs):
		
		lista_fields = []
		lista_fields.append(["command", request.get_argument('command', '')])

		lista_files = []
		lista_files.append(["file", files])
		#lista_files.append(["file", request.files['file'][0]])
		
		print("\n\n\nLe form:\n\n\n")
		
		body, headers = self.create_body(lista_fields, lista_files)
		url ="http://localhost:8080/send_file"
		import urllib.request
		import http.client
		req = urllib.request.Request (url)
		connection = http.client.HTTPConnection (req.host)
		connection.request ('POST', req.selector, body, headers)
		response = connection.getresponse ()
		print(response)
		request.finish("file" + "Patata" + " is uploaded")
		return

		#http://stackoverflow.com/a/28613273/2628463
		import mimetypes
		def encode_multipart_formdata(fields, files):
			"""
			fields is a sequence of (name, value) elements for regular form fields.
			files is a sequence of (name, filename, value) elements for data to be
			uploaded as files.
			Return (content_type, body) ready for httplib.HTTP instance
			"""
			BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
			CRLF = '\r\n'
			L = []
			"""for (key, value) in fields:
				L.append('--' + BOUNDARY)
				L.append('Content-Disposition: form-data; name="%s"' % key)
				L.append('')
				L.append(value)"""
			for (key, filename, value) in files:
				filename = filename.encode("utf8")
				L.append('--' + BOUNDARY)
				L.append(
					'Content-Disposition: form-data; name="%s"; filename="%s"' % (
						key, filename
					)
				)
				L.append('Content-Type: %s' % get_content_type(filename))
				L.append('')
				L.append(value)
			L.append('--' + BOUNDARY + '--')
			L.append('')
			body = CRLF.join(L)
			content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
			return content_type, body


		def get_content_type(filename):
			try:
				return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
			except TypeError:
				return 'application/octet-stream'
		content_type, body = encode_multipart_formdata(fields, files)
		#headers = {"Content-Type": content_type, 'content-length': str(len(body))}
		#request = HTTPRequest(url, "POST", headers=headers, body=body, validate_cert=False)
		print(content_type)
		print(body)
		import time
		time.sleep(10)
		print("End sleep")
		request.finish("file" + "Patata" + " is uploaded")
		#callback()