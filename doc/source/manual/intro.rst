Manual
======

The application divides the functionality between two executables: ``deployer`` (as the ``marcodeployerd`` daemon) and ``receiver`` (``marcoreceiverd``). The first one handles the user interaction and the issuing of deployment actions (as well as the **statusmonitor** and **shell** backends), whereas the latter receives the commands, handles the deployment and returns the **statusmonitor** and **shell** data. Both roles can exist in the same node.

The published **MarcoPolo** services are the following:

- **marcodeployerd**: service deployer, on port 1443 (redirected to 1342 for HTTPS).
- **marcoreceiverd**: service receiver on ports 1339 and 1370 (websocket) and service statusmonitor on port 1370 (the same websocket connection as the receiver service).

.. toctree::
	:maxdepth: 2

	statusmonitor
	deployer
	logger
	receiver