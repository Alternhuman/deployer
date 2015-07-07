Technical details
=================

Security concerns
-----------------

All communications (except the Marco discovery and the initial HTTP entry point) go through a secure HTTPS (or WSS) channel. In order to reduce the number of times that the user must input his access credentials, client certificate validation is used in the channel between the backend and the receiver.

The production certificates may be self-signed. If so, the WebSocket connection must be manually validated during the first connection. A message like this will be displayed:

.. image:: ../img/connection_error.*
	:align: center

After clicking, a "probing" windown will be displayed, and the browser will warn that the certificate is not trusted.

.. image:: ../img/validate_certificate_1.*
	:align: center

After adding the certificate to the list of trusted identities, the probing window displays a confirmation message.

.. image:: ../img/validate_certificate_2.*
	:align: center

Authentication
--------------

The application uses PAM to validate the user credentials. If there is no instance of PAM in the system, the files ``/etc/passwd`` and ``/etc/shadow`` will be used instead. 