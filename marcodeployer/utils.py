#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
from crypt import crypt
from re import compile as compile_regex

import pam
import netifaces as ni
from netifaces import AF_INET

#http://code.activestate.com/recipes/578489-system-authentication-against-etcshadow-or-etcpass/
def authenticate(name, password):
    """
    Returns true or false depending on the success of the name-password combination using
    the shadows or passwd file (The shadow file is preferred if it exists) 
    """
    try:
        success = pam.pam().authenticate(name, password)
        if success is True:
            return success
    except Exception as e:
        print("Exception")
        print(e)
        return False
        
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
        print("AttributeError")
        return False
    print("Returning")
    return crypt(password, salt) == shadow


def getip(interface, protocol=None, host=None):
    """
    Returns the IP associated with the configured interface
    """
    return ni.ifaddresses(interface).get(AF_INET)[0].get('addr')
