#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from web.controller import process

if __name__ == "__main__":
    web_server = process.WebServer()
    if web_server.setup_tcp('360WiFi-EE3B0D', 'ccdroid91', '8080'):
        web_server.action()
    else:
        print("Failed to start web server.")
