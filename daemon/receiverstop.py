#!/usr/bin/env python3
# -*- coding: utf-8
from os import kill, remove
import os

PIDFILE = '/var/run/deployer/receiver.pid'

f = open(PIDFILE, 'r')
pid = f.read()
f.close()
kill(int(pid), 2)
os.remove(PIDFILE)
