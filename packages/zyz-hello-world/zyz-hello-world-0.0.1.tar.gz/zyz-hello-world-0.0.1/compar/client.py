#!/usr/bin/env python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto('Hello'.encode('utf-8'), ('127.0.0.1', 60011))


sock.close()
