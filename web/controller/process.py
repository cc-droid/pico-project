import utime
from machine import Pin
from modules import network
from web.model import model
import re
import uasyncio as asyncio

class WebServer:
    def __init__(self):
        self.network = network.Network()
        self.model = model.DataModel()
        self.connection_id = 0
        self.lock = asyncio.Lock() # 创建一个锁
        print("Web_server init.....")

    def setup_tcp(self, ssid, password, port):
        self.network.setup_wifi_server(ssid, password, port)
        print("setup_tcp successful.")
        return True

    def process_request(self, request, led):
        request = request.lower()  # Normalize request string
        if re.match(r'^/$', request):
            print("Processing root request.")
            return "OK"
        elif re.match(r'^/lighton\??$', request):
            print("LED on")
            try:
                led.value(1)
                self.model.toggle_led("ON")
                return "ON"
            except Exception as e:
                print(f"Error turning on LED: {e}")
                return None
        elif re.match(r'^/lightoff\??$', request):
            print("LED off")
            try:
                led.value(0)
                self.model.toggle_led("OFF")
                return "OFF"
            except Exception as e:
                print(f"Error turning off LED: {e}")
                return None
        elif re.match(r'^/value\??$', request):
            value = self.model.fetch_random_value()
            return value
        else:
            print("Unknown request:", request)
        return None

    def webpage(self, chunk_size=1024):
        try:
            with open('/web/view/index.html', 'r') as file:
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    chunk = chunk.replace("{state}", self.model.state)
                    chunk = chunk.replace("{random_value}", str(self.model.random_value))
                    yield chunk
        except OSError as e:
            print(f"Error reading HTML file: {e}")
            yield "<html><body><h1>Error loading page</h1></body></html>"

    async def action(self):
        try:
            led = Pin('LED', Pin.OUT)
        except Exception as e:
            print(f"Error initializing LED: {e}")
            return

        print("Action loop started...")
        while True:
            try:
                await self.lock.acquire()  # 获取锁
                try:
                    self.connection_id, res = self.network.esp_rcvData()
                    await asyncio.sleep(0.2)
                finally:
                    self.lock.release()  # 释放锁

                request = str(res) if self.connection_id is not None else ""

                if request:
                    print(f'Request content: {request}')
                    try:
                        request = request.split()[1]
                        print(f'Request: {request}')
                    except IndexError as e:
                        print(f'Request parsing error: {e}')
                        continue

                    recv = self.process_request(request, led)
                    if recv is not None:
                        if isinstance(recv, int):
                            self.model.random_value = recv
                        else:
                            self.model.state = recv

                        print(f"Current state: {self.model.state}")
                        
                        webpage_content = ''.join(self.webpage())
                        content_length = len(webpage_content)
                        await self.lock.acquire()  # 获取锁
                        try:
                            # 发送 HTTP 响应头
                            self.network.esp_sendData(self.connection_id, f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {content_length}\r\n\r\n')
                            await asyncio.sleep(0.2)  # 确保发送过程平稳，避免设备负载过高
                        finally:
                            self.lock.release()  # 释放锁


                        for chunk in self.webpage():
                            await self.lock.acquire()  # 获取锁
                            try:
                                self.network.esp_sendData(self.connection_id, chunk)
                                await asyncio.sleep(0.2)  # 确保发送过程平稳，避免设备负载过高
                            finally:
                                self.lock.release()  # 释放锁

                        self.network.esp_sendData(self.connection_id, '\r\n')  # 发送结束标志
                        await asyncio.sleep(0.2)  # 添加适当的延迟以避免过载


            except OSError as e:
                print(f'Connection error: {e}')
            except Exception as e:
                print(f'Unexpected error: {e}')
