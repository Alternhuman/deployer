Logger
======

The logger functionality comprises two main views of the application.

The logger tab
--------------

The `Logger` tab outputs the commands during the deployment. Each node has a subtab with a window per process. Clicking on the button stops the execution.

.. image:: ../img/logger-deployer.*
    :align: center

The shell tab
-------------

The Shell view allows the execution of commands without performing any deployment. The shell is relative to the home of the user and all commands are executed with his UID and GID. The working principle is identical to the Logger tab.

.. image:: ../img/logger-shell.*
    :align: center 