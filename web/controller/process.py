# controller/web.py
import utime
from machine import Pin
from modules import network
from web.model import model

class WebServer:
    def __init__(self):
        self.network = network.Network()
        self.model = model.DataModel()
        self.connection_id = 0
        print("Web_server init.....")

    def setup_tcp(self, ssid, password, port):
        self.network.setup_wifi_server(ssid, password, port)
        print("setup_tcp.....")

    def process_request(self, request, led):
        if request == '/':
            print("process /++++++++++")
            return "OK"
        elif request == '/lighton?':
            print("LED on")
            led.value(1)
            self.model.toggle_led("ON")
            return "ON"
        elif request == '/lightoff?':
            print("LED off")
            led.value(0)
            self.model.toggle_led("OFF")
            return "OFF"
        elif request == '/value?':
            value = self.model.fetch_random_value()
            return value
        else:
            print("process_error:", request)
        return None

    def webpage(self):
        html = open('/web/view/index.html', 'r').read()
        html = html.replace("{state}", self.model.state)
        html = html.replace("{random_value}", str(self.model.random_value))
        return html

    def action(self):
        led = Pin('LED', Pin.OUT)

        print("action init...")
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
                        # Update model state based on response
                        if isinstance(recv, int):
                            self.model.random_value = recv
                        else:
                            self.model.state = recv
                        
                        print("Current state:", self.model.state)
                        # Generate HTML response
                        response = self.webpage()  
                        # Send the HTTP response and close the connection
                        print("process 1:", self.connection_id)
                        self.network.esp_sendData(self.connection_id, 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                        utime.sleep_ms(300)
                        print("process 2:", self.connection_id)
                        self.network.esp_sendData(self.connection_id, response)
                        utime.sleep_ms(300)
                        print("process 3:", self.connection_id)
            except OSError as e:
                print('Connection closed:', e)