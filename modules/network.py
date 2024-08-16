import utime
from machine import UART

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