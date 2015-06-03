Installation
============

The installation of the deployer is rather easy when using a package manager such as `pacman <https://wiki.archlinux.org/index.php/Pacman>`_ or `apt <https://wiki.debian.org/Apt>`_, and it suffices with the following to install it:

..TODO: do the installing part

It can also be installed through the `setup.py` script that is included on the tarball.

The deployer role is activated by default. The receiver, however, is not. To activate it the following command has to be issued:

..TODO command

The package requires the following dependencies to be set up:

- certifi==2015.4.28

- netifaces==0.10.4

- pyjade==3.0.0

- python-pam==1.8.2

- requests==2.7.0

- requests-futures==0.9.5

- six==1.9.0

- tornado==4.1

- marcopolo==0.1 (and to work, polo must be running before the receiver is started. So must marco for the deployer).

The package runs successfuly on both Python 2 and 3. However, most of the testing process has been done on Python 3 only, and it is not guaranteed complete functionaly on Python 2.

The package creates the following files:

- A service file in `/etc/init.d` or `/etc/systemd/system`

- The executables on `/usr/sbin`

- The modules on the Python modules folder

- During execution runfiles are stored in `/var/run` and logs are stored in `/var/log`