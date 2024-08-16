from modules import network

class Sample:
    def __init__(self):
        pass
    def tcp_client(self, ssid, password, server_ip, port, network = network.Network()): 
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

    def tcp_server(self, ssid, password, port, network = network.Network()):
        network.setup_wifi_server(ssid, password, port)  # 调用设置WiFi连接的函数

        while True:
            ID,s_get = network.esp_rcvData()            # 接收数据
            if(ID != None):
                network.esp_sendData(ID,s_get)            # 如果接收到的数据不为空，则回传

    def udp_sample(self, ssid, password, remote_ip, remote_port, local_port, network = network.Network()): 
        network.setup_wifi_udp(ssid, password, remote_ip, remote_port,local_port)  # 调用设置WiFi连接的函数

        network.esp_uart.write('Hello makerobo !!!\r\n')       # 发送对应的字符串
        network.esp_uart.write('RP2040 UDP message!\r\n')
        while True:
            s_get=network.esp_uart.read()              # 接收字符
            if(s_get != None):                         # 判断字符不为空
                s_get=s_get.decode()
                print(s_get)                           # 字符串打印
                network.esp_uart.write(s_get)          # 字符串回传