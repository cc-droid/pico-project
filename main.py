#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uasyncio
from web.controller import process


async def blink_led():
    while True:
        print("led blink")
        await uasyncio.sleep(3)  # Blink interval


async def main():    
    while True:
        # Add other tasks that you might need to do in the loop
        await uasyncio.sleep(5)
        print('This message will be printed every 5 seconds')

async def do_web():    
    web_server = process.WebServer()
    if web_server.setup_tcp('360WiFi-EE3B0D', 'ccdroid91', '8080'):
        print('Setting up server')
    else:
        print("Failed to start web server.")

    await web_server.action()
    

# Create an Event Loop
loop = uasyncio.get_event_loop()
# Create a task to run the main function
loop.create_task(main())
loop.create_task(do_web())
loop.create_task(blink_led())

try:
    # Run the event loop indefinitely
    loop.run_forever()
except Exception as e:
    print('Error occured: ', e)
except KeyboardInterrupt:
    print('Program Interrupted by the user')
