#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
from crypt import crypt
from re import compile as compile_regex

import pam

#http://code.activestate.com/recipes/578489-system-authentication-against-etcshadow-or-etcpass/
def authenticate(name, password):
	"""
	Returns true or false depending on the success of the name-password combination using
	the shadows or passwd file (The shadow file is preferred if it exists) 
	"""
	return pam.pam().authenticate(name, password)

	if path.exists("/etc/shadow"):
		import spwd
		shadow = spwd.getspnam(name).sp_pwdp # https://docs.python.org/3.4/library/spwd.html#module-spwd
	else:
		import pwd
		shadow = pwd.getpwnam(name).pw_passwd
	
	salt_pattern = compile_regex(r"\$.*\$.*\$")
	
	try:
		salt = salt_pattern.match(shadow).group()
	except AttributeError:
		return False

	return crypt(password, salt) == shadow