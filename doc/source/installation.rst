Installation
============

The installation of the software is rather easy when using a package manager. Only pip (`pypi.python.org/pypi/pip <https://pypi.python.org/pypi/pip>`_) is available at the moment, and it suffices with the following command to install it.

::
    
    pip install marcopolo-deployer


It can also be installed through the ``setup.py`` script that is included on the tarball with the following command:

::
    
    python setup.py install

The *deployer* role is activated by default. The *receiver*, however, is not. To activate it the following commands have to be issued.

**systemd**:

::
    
    systemctl enable marcoreceiverd
    systemctl start marcoreceiverd
    
**init.d**

::

    update-rc.d marcoreceiverd defaults
    /etc/init.d/marcoreceiverd start


The package requires the following dependencies to work. They will be downloaded during the installation:

::

    certifi==2015.4.28
    netifaces==0.10.4
    pyjade==3.0.0
    python-pam==1.8.2
    requests==2.7.0
    requests-futures==0.9.5
    six==1.9.0
    tornado==4.1
    marcopolo>=0.1
    marcopolo.bindings>=0.0.1

The package runs has been tested successfuly on both Python 2.7 and 3.4. Compatibility with older versions is not guaranteed.

The package creates the following files:

- A service file in ``/etc/init.d`` or ``/etc/systemd/system`` for each of the daemons.
- The executables (entry points to the modules) on ``/usr/bin``.
- The modules on the Python modules folder.
- During execution runfiles are stored in ``/var/run`` and logs are stored in ``/var/log``.
- The configuration files are in  ``/etc/marcodeployer/deployer.cfg``. :doc:`Here <configuration>` is an example of the configuration file.
- The JavaScript, fonts, images and CSS code are located in ``/usr/lib/marcodeployer/static``.
- The Jade templates used by the utility are located in ``/usr/lib/marcodeployer/templates``.

Certificates
------------

The required certificates are located in ``/usr/lib/marcodeployer/certs``. **The included certificates are not suited for production use**. Replace them with your own set of certificates for any purpose other than trying the application, or the security of your entire system might be compromised.