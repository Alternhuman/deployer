Receiver
========

The receiver does not provide any user interface (except the probing pages). It simply provides an HTTP-based interface for the deployment of files and issuing of commands and a WebSocket channel for asynchronous communications. Each time a client connects to the deployer, a WebSocket connection to each receiver is created, which lasts for the whole session.
