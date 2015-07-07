Configuration
=============

The software is modified through a file located in ``/etc/marcodeployer/deployer.cfg``. Only one file provides configuration for the both roles.

This is an example of a configuration file:

.. literalinclude:: ../../etc/marcodeployer/deployer.cfg

The file has three sections. ``common`` are parameters used by both the deployer and receiver roles and it simply includes some directory paths for certificates, logging and temporary files. ``deployer`` stores regarding the deployer and ``receiver`` does the same for the receiver role.

All paths for logging and certificate handling can be either absolute or relative. They will be relative to the value of the ``certs``, ``tmpdir`` or ``logging_dir`` variables.

The values in the example are also the used by the software as defaults if the parameter is not specified in the configuration file.