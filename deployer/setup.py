#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The deployer application
"""

from setuptools import setup, find_packages
from distutils.core import setuptools
from distutils.command.clean import clean
from distutils.command.install import install
from codecs import open
import os, sys, subprocess
import glob

custom_deployer_params = [
                            "--deployer-disable-daemons",
                            "--deployer-disable-deployer",
                            "--deployer-enable-receiver",
                            "--deployer-no-start"
                         ]

def detect_init():
    try:
        subprocess.check_call(["systemctl", "--version"], stdout=None, stderr=None, shell=False)
        return 0
    except (subprocess.CalledProcessError, OSError):
        return 1

def enable_service(service):
    sys.stdout.write("Enabling service " + service +"...")
    if init_bin == 0:
        subprocess.call(["systemctl", "enable", service], shell=False)
    else:
        subprocess.call(["update-rc.d", "-f", service, "remove"], shell=False)
        subprocess.call(["update-rc.d", service, "defaults"], shell=False)
    
    sys.stdout.write("Enabled!\n")

def start_service(service):
    sys.stdout.write("Starting service " + service + "...")
    if init_bin == 0:
        subprocess.call(["systemctl", "start", service], shell=False)
    else:
        subprocess.call(["update-rc.d", service, "start"], shell=False)

    sys.stdout.write("Started!\n")

if __name__ == "__main__":

    deployer_params = []

    python_version = int(sys.version[0])

    for param in sys.argv:
        if param in custom_marcopolo_params:
            deployer_params.append(param)
            sys.argv.remove(param)

    here = os.path.abspath(os.path.dirname(__file__))

    long_description = ""
    
    with open(os.path.join(here, "DESCRIPTION.rst"), encoding='utf-8') as f:
        long_description = f.read()

    def copy_dir(directory, module):
        dir_path = directory
        base_dir = os.path.join(module, dir_path)
        for (dirpath, dirnames, files) in os.walk(base_dir):
            for f in files:
                yield os.path.join(dirpath.split('/', 1)[1], f)

    data_files = [
                    ('/usr/lib/deployer/static/css', [f for f in copy_dir('static/css', 'deployer')]),
                    ('/usr/lib/deployer/static/fonts', [f for f in copy_dir('static/fonts', 'deployer')]),
                    ('/usr/lib/deployer/static/img', [f for f in copy_dir('static/img', 'deployer')]),
                    ('/usr/lib/deployer/static/js', [f for f in copy_dir('static/js', 'deployer')]),
                    ('/usr/lib/deployer/certs', [os.path.join("certs", f) for f in os.listdir("certs")])
                 ]
    
    # if "--marcopolo-disable-daemons" not in marcopolo_params:
    #     init_bin = detect_init()
    #     if python_version == 2:
    #         if init_bin == 1:
    #             daemon_files = [
    #                              ('/etc/init.d/', ["daemon/systemv/marcod", "daemon/systemv/polod"])
    #                            ]

    #         else:
    #             daemon_files = [('/etc/systemd/system/', ["daemon/marco.service", "daemon/polo.service"]),
    #                              ('/usr/local/bin/', glob.glob("daemon/*.py"))
    #                            ]
            
    #         data_files.extend(daemon_files)

    #         twistd_files = [('/etc/marcopolo/daemon', ["daemon/twistd/marco_twistd.tac", 
    #                                                    "daemon/twistd/polo_twistd.tac"])
    #                        ]
    #         data_files.extend(twistd_files)

    #     elif python_version == 3:
    #         if init_bin == 1:
    #             daemon_files = [
    #                              ('/etc/init.d/', ["daemon/python3/systemv/marcod", "daemon/python3/systemv/polod"])
    #                            ]

    #         else:
    #             daemon_files = [('/etc/systemd/system/', ["daemon/python3/marco.service", "daemon/python3/polo.service"]),
    #                              ('/usr/local/bin/', glob.glob("daemon/python3/*.py"))
    #                            ]
            
    #         data_files.extend(daemon_files)

    description = "The deployer for the marcopolo environment"

    setup(
        name="marcodeployer",
        provides=["marcodeployer"],
        version='0.0.1',
        description=description,
        long_description = long_description,
        url="marcopolo.martinarroyo.net/apps/marcodeployer",
        author="Diego Martín",
        author_email="martinarroyo@usal.es",
        license="MIT",
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',

        ],
        keywords="marcopolo deployer",
        packages=find_packages(),
        install_requires=[
            'certifi==2015.4.28',
            'netifaces==0.10.4',
            'pyjade==3.0.0',
            'python-pam==1.8.2',
            'requests==2.7.0',
            'requests-futures==0.9.5',
            'six==1.9.0',
            'tornado==4.1',
            'marcopolo',
            'marcopolobindings'
        ],
        zip_safe=False,
        data_files=data_files,
        entry_points={
            'console_scripts':[
                'marcodeployer = marcodeployer.deployer:main',
                'marcoreceiver = marcodeployer.receiver:main'
            ]
        }
    )

    # if "--marcopolo-disable-daemons" not in marcopolo_params:
    #     if "--marcopolo-disable-marco" not in marcopolo_params:
    #         enable_service("marcod")
    #         if "--marcopolo-no-start" not in marcopolo_params:
    #             start_service("marcod")

    #     if "--marcopolo-enable-polo" in marcopolo_params:
    #         enable_service("polod")
    #         if "--marcopolo-no-start" not in marcopolo_params:
    #             start_service("polod")

    # if not os.path.exists("/var/log/marcopolo"):
    #     os.makedirs('/var/log/marcopolo')