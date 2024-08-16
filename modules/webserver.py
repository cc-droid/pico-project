import random
import utime
from machine import Pin
from modules import network

class Web_server:
    def __init__(self):
        self.network = network.Network()
        self.state = "OFF"
        self.random_value = 0
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