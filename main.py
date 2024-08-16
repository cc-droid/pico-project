#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time,utime
import random
from machine import UART,Pin

class Network:
    def __init__(self, uart_port=0, baud_rate=115200):
        self.esp_uart = UART(uart_port, baud_rate)  # 初始化串口

    # 发送命令函数
    def esp_sendCMD(self, cmd, ack, timeout=2000):
        self.esp_uart.write(cmd + '\r\n')
        start_time = utime.ticks_ms()
        while (utime.ticks_ms() - start_time) < timeout:
            response = self.esp_uart.read()
            if response is not None:
                response = response.decode()
                print(response)
                if response.find(ack) >= 0:
                    return True
        return False
    
    # 发送数据
    def esp_sendData(self, ID, data):
        self.esp_sendCMD('AT+CIPSEND='+str(ID)+','+str(len(data)),'>')
        self.esp_uart.write(data)

        # 接收数据
    def esp_rcvData(self):
        s_get= self.esp_uart.read()
        if(s_get != None):
            s_get=s_get.decode()
            print(s_get)
            if(s_get.find('+IPD') >= 0):
                n1=s_get.find('+IPD,')
                n2=s_get.find(',',n1+5)
                ID=int(s_get[n1+5:n2])
                n3=s_get.find(':')
                s_get=s_get[n3+1:]
                return ID,s_get
        return None,None
    
    def init_wifi(self):
        self.esp_uart.write('+++')  # 初始化退出透传模式
        utime.sleep(1)
        if self.esp_uart.any() > 0:
            self.esp_uart.read()

    # 设置WiFi tcp client连接函数，加入参数
    def setup_wifi_client(self, ssid, password, server_ip, port):
        self.init_wifi()
        # 执行WiFi连接命令
        self.esp_sendCMD("AT", "OK")  # AT指令
        self.esp_sendCMD("AT+CWMODE=3", "OK")  # 配置 WiFi 模式
        self.esp_sendCMD(f'AT+CWJAP="{ssid}","{password}"', "OK", 20000)  # 连接路由器
        self.esp_sendCMD("AT+CIFSR", "OK")  # 查询 WIFI模块的 IP 地址
        self.esp_sendCMD(f'AT+CIPSTART="TCP","{server_ip}",{port}', "OK", 10000)  # 连接到服务器
        self.esp_sendCMD("AT+CIPMODE=1", "OK")  # 开启透传模式
        self.esp_sendCMD("AT+CIPSEND", ">")  # 准备发送数据

        # 设置WiFi tcp server连接函数，加入参数
    def setup_wifi_server(self, ssid, password, port):
        self.init_wifi()
        self.esp_sendCMD("AT","OK")           # AT指令
        self.esp_sendCMD("AT+CWMODE=3","OK")  # 配置 WiFi 模式
        self.esp_sendCMD("AT+CWJAP=\""+ssid+"\",\""+password+"\"","OK",20000) # 连接路由器
        self.esp_sendCMD("AT+CIPMUX=1","OK")            # 使能多连接
        self.esp_sendCMD("AT+CIPSERVER=1,"+port,"OK")   # 建⽴ TCP server
        self.esp_sendCMD("AT+CIFSR","OK")               # 查询 WIFI模块的 IP 地址

    # 设置WiFi udp 连接函数，加入参数
    def setup_wifi_udp(self, ssid, password, remote_ip,remote_port, local_port):
        self.init_wifi()

        self.esp_sendCMD("AT","OK")          # AT指令
        self.esp_sendCMD("AT+CWMODE=3","OK") # 配置 WiFi 模式
        self.esp_sendCMD("AT+CWJAP=\""+ssid+"\",\""+password+"\"","OK",20000) # 连接路由器
        self.esp_sendCMD("AT+CIFSR","OK")                                     # 查询 WIFI模块的 IP 地址
        #self.esp_sendCMD("AT+CIPSTART=\"UDP\",\""+remote_ip+"\","+remote_port+","+local_port+",0","OK",10000) # 创建 UDP 传输
        self.esp_sendCMD("AT+CIPSTART=\"UDP\",\""+remote_ip+"\","+str(remote_port)+","+str(local_port)+",0","OK",10000)
        self.esp_sendCMD("AT+CIPMODE=1","OK")    # 开启透传模式，数据可以直接传输
        self.esp_sendCMD("AT+CIPSEND",">")       # 发送数据

class Sample:
    def __init__(self):
        pass
    def tcp_client(self, ssid, password, server_ip, port, network = Network()): 
        network.setup_wifi_client(ssid, password, server_ip, port)  # 调用设置WiFi连接的函数
        # 发送数据
        network.esp_uart.write('Hello makerobo !!!\r\n')  # 发送相关内容
        network.esp_uart.write('RP2040-W TCP Client\r\n')

        # 持续读取服务器响应
        while True:
            incoming_data = network.esp_uart.read()
            if incoming_data is not None:
                incoming_data = incoming_data.decode()
                print(incoming_data)

    def tcp_server(self, ssid, password, port, network = Network()):
        network.setup_wifi_server(ssid, password, port)  # 调用设置WiFi连接的函数

        while True:
            ID,s_get = network.esp_rcvData()            # 接收数据
            if(ID != None):
                network.esp_sendData(ID,s_get)            # 如果接收到的数据不为空，则回传

    def udp_sample(self, ssid, password, remote_ip, remote_port, local_port, network = Network()): 
        network.setup_wifi_udp(ssid, password, remote_ip, remote_port,local_port)  # 调用设置WiFi连接的函数

        network.esp_uart.write('Hello makerobo !!!\r\n')       # 发送对应的字符串
        network.esp_uart.write('RP2040 UDP message!\r\n')
        while True:
            s_get=network.esp_uart.read()              # 接收字符
            if(s_get != None):                         # 判断字符不为空
                s_get=s_get.decode()
                print(s_get)                           # 字符串打印
                network.esp_uart.write(s_get)          # 字符串回传

class Web_server:
    def __init__(self):
        self.network = Network()
        self.state = "OFF"
        self.random_value = 0
        self.connection_id = 0

    def setup_tcp(self, ssid, password, port):
        self.network.setup_wifi_server(ssid, password, port)

    def process_request(self, request, led):
        if request == '/':
            print("process /++++++++++")
            return "OK"
        elif request == '/lighton?':
            print("LED on")
            led.value(1)
            return "ON"
        elif request == '/lightoff?':
            led.value(0)
            return 'OFF'
        elif request == '/value?':
            return random.randint(0, 20)
        else:
            print("process_error:", request)
        return None

        # HTML template for the webpage
    def webpage(self):
        html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>IOT Server</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
                <h1>IOT Server</h1>
                <h2>Led Control</h2>
                <form action="./lighton">
                    <input type="submit" value="Light on" />
                </form>
                <br>
                <form action="./lightoff">
                    <input type="submit" value="Light off" />
                </form>
                <p>LED state: {self.state}</p>
                <h2>Fetch New Value</h2>
                <form action="./value">
                    <input type="submit" value="Fetch value" />
                </form>
                <p>Fetched value: {self.random_value}</p>
            </body>
            </html>
            """
        return str(html)
    
    def action(self):
        led = Pin('LED', Pin.OUT)

        while True:
            try:
                self.connection_id, res = self.network.esp_rcvData()
                request = str(res) if self.connection_id is not None else ""

                if request != "":
                    print('Request content = %s' % request)
                    try:
                        request = request.split()[1]
                        print('Request:', request)
                    except IndexError:
                        print('Request_error:', request)
                    recv = self.process_request(request, led)
                    if recv is not None:
                        if type(recv) == int:
                            self.random_value = recv
                        else:
                            self.state = recv
                        
                        print("Current state:", self.state)
                        # Generate HTML response
                        response = self.webpage()  
                        # Send the HTTP response and close the connection
                        print("process 1:",self.connection_id)
                        self.network.esp_sendData(self.connection_id,'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')  # 如果接收到的数据不为空，则回传
                        utime.sleep_ms(300)
                        print("process 2:",self.connection_id)
                        self.network.esp_sendData(self.connection_id, response)
                        utime.sleep_ms(300)
                        print("process 3:",self.connection_id)
            except OSError as e:
                print('Connection closed:', e)
    


# 主程序入口
if __name__ == "__main__":
    #sample = Sample()
    #sample.tcp_client('360WiFi-EE3B0D','ccdroid91','192.168.8.94', '8080')
    #sample.tcp_server('360WiFi-EE3B0D','ccdroid91', '8080')
    #sample.udp_sample('360WiFi-EE3B0D','ccdroid91', '192.168.8.94', 8080, 1010)

    web_server = Web_server()
    web_server.setup_tcp('360WiFi-EE3B0D','ccdroid91', '8080')
    web_server.action()