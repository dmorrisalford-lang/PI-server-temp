"""DHT11 Temperature and Humidity Sensor Server for Raspberry Pi Pico W 2
MicroPython implementation for reading DHT11 sensor and creating a simple HTTP server
"""

import network
import socket
import time
from dht import DHT11
from machine import Pin

# WiFi configuration
WIFI_SSID = 'YOUR_SSID'
WIFI_PASSWORD = 'YOUR_PASSWORD'

# GPIO pin configuration for DHT11 (GPIO15 = Pin 20 on Pico W)
dht_pin = Pin(15, Pin.IN, Pin.PULL_UP)
dht = DHT11(dht_pin)

# Global variables for sensor readings
temperature = 0
humidity = 0
last_read_time = 0

def connect_wifi():
    """Connect to WiFi network"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    print(f'Connecting to {WIFI_SSID}...')
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    # Wait for connection
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(1)
    
    if wlan.status() == 3:
        print('Connected successfully')
        status = wlan.ifconfig()
        print(f'IP Address: {status[0]}')
        return True
    else:
        print('Failed to connect to WiFi')
        return False

def read_sensor():
    """Read temperature and humidity from DHT11"""
    global temperature, humidity, last_read_time
    
    try:
        dht.measure()
        temperature = dht.temperature()
        humidity = dht.humidity()
        last_read_time = time.time()
        print(f'Temperature: {temperature}°C, Humidity: {humidity}%')
        return True
    except Exception as e:
        print(f'Error reading DHT11: {e}')
        return False

def html_page():
    """Generate HTML response"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Pi Pico W DHT11 Monitor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family: Arial; text-align: center; margin-top: 50px; }}
        .container {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        h1 {{ color: #333; }}
        .sensor-data {{ font-size: 24px; margin: 20px 0; }}
        .temperature {{ color: #e74c3c; }}
        .humidity {{ color: #3498db; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Raspberry Pi Pico W</h1>
        <h2>DHT11 Sensor Monitor</h2>
        <div class="sensor-data">
            <p class="temperature">Temperature: {temperature}°C</p>
            <p class="humidity">Humidity: {humidity}%</p>
        </div>
        <p><small>Last update: {time.localtime()}</small></p>
    </div>
</body>
</html>"""
    return html

def start_server(port=80):
    """Start HTTP server"""
    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(1)
    
    print(f'Server listening on port {port}')
    
    try:
        while True:
            # Read sensor every 5 seconds
            if time.time() - last_read_time >= 5:
                read_sensor()
            
            # Handle incoming connections
            cl, addr = sock.accept()
            print(f'Connection from {addr}')
            
            request = cl.recv(1024).decode()
            print(f'Request: {request}')
            
            if 'GET' in request:
                response = f"""HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
{html_page()}"""
                cl.send(response.encode())
            
            cl.close()
    
    except KeyboardInterrupt:
        print('Server stopped')
        sock.close()

if __name__ == '__main__':
    print('Initializing Pi Pico W DHT11 Server...')
    
    if connect_wifi():
        read_sensor()  # Initial read
        start_server()
    else:
        print('Failed to initialize server')
