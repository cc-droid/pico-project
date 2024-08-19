from machine import Pin
from modules import network
from web.model import model
import re
import uasyncio as asyncio
from web.view.index import get_index_html
from web.view.dev_ctl import get_dev_ctl_html
from web.view.setting import get_setting_html
from web.view.err import get_404_html  # 导入 404 页面生成函数

class WebServer:
    def __init__(self):
        self.network = network.Network()
        self.model = model.DataModel()
        self.connection_id = 0
        self.lock = asyncio.Lock()  # 创建一个锁
        print("Web_server init.....")

    def setup_tcp(self, ssid, password, port):
        self.network.setup_wifi_server(ssid, password, port)
        print("setup_tcp successful.")
        return True

    def process_request(self, request, led):
        request = request.lower()  # Normalize request string
        if request == "/":
            print("Processing root request.")
            return "index"
        elif request.startswith("/dev_ctl"):
            print("Processing device control request.")
            return "dev_ctl"
        elif request.startswith("/setting"):
            print("Processing settings request.")
            return "setting"
        elif request == "/lighton?":
            print("LED on")
            try:
                led.value(1)
                self.model.toggle_led("ON")
                return "ON"
            except Exception as e:
                print(f"Error turning on LED: {e}")
                return None
        elif request == "/lightoff?":
            print("LED off")
            try:
                led.value(0)
                self.model.toggle_led("OFF")
                return "OFF"
            except Exception as e:
                print(f"Error turning off LED: {e}")
                return None
        elif request == "/value?":
            value = self.model.fetch_random_value()
            return value
        elif request == "/favicon.ico":
            # 处理 favicon.ico 请求，返回 204 No Content
            print("Favicon requested, returning 204 No Content.")
            return "204"  # 返回一个特殊标识符
        else:
            print("Unknown request:", request)
            return "404"  # 返回 404 标识符

    def webpage(self, chunk_size=1536):
        if self.model.state == "index":
            # 使用示例数据
            pico_info = {
                'model': 'Raspberry Pi Pico',
                'micropython_version': '1.19.1',
                'cpu_frequency': 133,  # MHz
                'memory_size': 2048,   # KB
                'temperature': 25       # °C
            }

            esp_info = {
                'firmware': 'ESP8266 AT Firmware',
                'free_memory': 512,     # KB
                'temperature': 30       # °C
            }

            weather_info = {
                'temperature': 22,      # °C
                'humidity': 60,        # %
                'condition': 'Clear'
            }

            html_content = get_index_html(pico_info, esp_info, weather_info)
        elif self.model.state == "dev_ctl":
            html_content = get_dev_ctl_html(self.model.state, self.model.random_value)
        elif self.model.state == "setting":
            html_content = get_setting_html()
        else:
            pass

        # Yielding chunks of HTML content
        for i in range(0, len(html_content), chunk_size):
            yield html_content[i:i + chunk_size]

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
                    await asyncio.sleep(0.3)  # 减少延迟
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
                        if recv == "204":
                            # 处理 favicon.ico 请求，返回 204 No Content
                            try:
                                self.network.esp_sendData(self.connection_id, 'HTTP/1.1 204 No Content\r\n\r\n')
                                print("Sent 204 No Content for favicon.ico.")
                            except OSError as e:
                                print(f'Error sending 204 response: {e}')
                            continue  # 跳过后续处理

                        if recv == "404":
                            # 处理 404 请求
                            try:
                                error_page = get_404_html()
                                self.network.esp_sendData(self.connection_id, f'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {len(error_page)}\r\n\r\n{error_page}')
                                print("Sent 404 Not Found response.")
                            except OSError as e:
                                print(f'Error sending 404 response: {e}')
                            continue  # 跳过后续处理

                        if isinstance(recv, int):
                            self.model.random_value = recv
                        else:
                            if recv in ["index", "dev_ctl", "setting"]:
                                self.model.state = recv

                        print(f"Current state: {self.model.state}")
                        
                        webpage_content = ''.join(self.webpage())
                        content_length = len(webpage_content)

                        # 检查连接是否仍然有效
                        if self.connection_id is None:
                            print("Connection closed, skipping response.")
                            continue

                        try:
                            # 发送 HTTP 响应头
                            self.network.esp_sendData(self.connection_id, f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {content_length}\r\n\r\n')
                            await asyncio.sleep(0.3)  # 减少延迟
                        except OSError as e:
                            print(f'Error sending response header: {e}')
                            continue

                        # 分块发送响应内容
                        for chunk in self.webpage(chunk_size=1536):
                            await self.lock.acquire()  # 获取锁
                            try:
                                self.network.esp_sendData(self.connection_id, chunk)
                                await asyncio.sleep(0.3)  # 减少延迟
                            except OSError as e:
                                print(f'Error sending response chunk: {e}')
                                break
                            finally:
                                self.lock.release()  # 释放锁

                        self.network.esp_sendData(self.connection_id, '\r\n')  # 发送结束标志
                        await asyncio.sleep(0.3)  # 减少延迟

            except OSError as e:
                print(f'Connection error: {e}')
            except Exception as e:
                print(f'Unexpected error: {e}')