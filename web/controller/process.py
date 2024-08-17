import utime
from machine import Pin
from modules import network
from web.model import model
import re

class WebServer:
    def __init__(self):
        self.network = network.Network()
        self.model = model.DataModel()
        self.connection_id = 0
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

    def action(self):
        try:
            led = Pin('LED', Pin.OUT)
        except Exception as e:
            print(f"Error initializing LED: {e}")
            return

        print("Action loop started...")
        while True:
            try:
                self.connection_id, res = self.network.esp_rcvData()
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
                        self.network.esp_sendData(self.connection_id, 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                        utime.sleep(0.1)  # 确保发送过程平稳，避免设备负载过高

                        for chunk in self.webpage():
                            self.network.esp_sendData(self.connection_id, chunk)
                            utime.sleep(0.2)  # 确保发送过程平稳，避免设备负载过高

            except OSError as e:
                print(f'Connection error: {e}')
            except Exception as e:
                print(f'Unexpected error: {e}')
