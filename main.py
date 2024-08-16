#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import Pin
from web.controller import process


# 主程序入口
if __name__ == "__main__":
    #sample = Sample()
    #sample.tcp_client('360WiFi-EE3B0D','ccdroid91','192.168.8.94', '8080')
    #sample.tcp_server('360WiFi-EE3B0D','ccdroid91', '8080')
    #sample.udp_sample('360WiFi-EE3B0D','ccdroid91', '192.168.8.94', 8080, 1010)

    web_server = process.WebServer()
    web_server.setup_tcp('360WiFi-EE3B0D','ccdroid91', '8080')
    web_server.action()