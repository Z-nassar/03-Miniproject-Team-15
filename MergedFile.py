# main.py for Raspberry Pi Pico W
# Title: Pico Light Orchestra with LED + API Control

import machine
import time
import network
import json
import asyncio

# -------- Pins --------
ADC_PIN   = 26      # photoresistor node (GP26 / ADC0)
BUZZ_PIN  = 18      # passive piezo buzzer (PWM)
R_PIN     = 1
G_PIN     = 2
B_PIN     = 3

# -------- Buzzer config (notes) --------
C4 = 262
D4 = 294
E4 = 330
F4 = 349
G4 = 392
A4 = 440
B4 = 494
C5 = 523

# --- Hardware Setup ---
photo_sensor = machine.ADC(ADC_PIN)
buzzer_pin   = machine.PWM(machine.Pin(BUZZ_PIN))

R = machine.Pin(R_PIN, machine.Pin.OUT)
G = machine.Pin(G_PIN, machine.Pin.OUT)
B = machine.Pin(B_PIN, machine.Pin.OUT)

def show(r, g, b):
    R.value(1 if r else 0)
    G.value(1 if g else 0)
    B.value(1 if b else 0)

# --- Global State ---
api_note_task = None
alpha = 0.2
smoothed = photo_sensor.read_u16()

# --- WiFi Connection ---
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("BU Guest (unencrypted)")  # No password
    max_wait = 10
    print("Connecting to Wi-Fi...")
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        time.sleep(1)
    if wlan.status() != 3:
        raise RuntimeError("Network connection failed")
    else:
        ip_address = wlan.ifconfig()[0]
        print(f"Connected! Pico IP Address: {ip_address}")
        return ip_address

# --- Tone Helpers ---
def stop_tone():
    buzzer_pin.duty_u16(0)

async def play_api_note(frequency, duration_s):
    """Coroutine to play a note from an API call, can be cancelled."""
    try:
        print(f"API playing note: {frequency}Hz for {duration_s}s")
        buzzer_pin.freq(int(frequency))
        buzzer_pin.duty_u16(32768)  # 50% duty cycle
        await asyncio.sleep(duration_s)
        stop_tone()
        print("API note finished.")
    except asyncio.CancelledError:
        stop_tone()
        print("API note cancelled.")

# --- Light → LED + Tone Mapping ---
def light_to_tone_and_led():
    global smoothed
    raw = photo_sensor.read_u16()
    smoothed = int(alpha * raw + (1 - alpha) * smoothed)

    bright = 1.0 - (smoothed / 65535.0)
    bright = max(0.0, min(1.0, bright))

    if bright >= 0.90:
        freq, color = C5, (1, 0, 0)   # Red
    elif bright >= 0.80:
        freq, color = C5, (1, 0, 0)   # Red
    elif bright >= 0.70:
        freq, color = B4, (1, 0, 1)   # Purple
    elif bright >= 0.60:
        freq, color = A4, (0, 0, 1)   # Blue
    elif bright >= 0.50:
        freq, color = G4, (0, 0, 1)   # Blue
    elif bright >= 0.40:
        freq, color = F4, (0, 1, 0)   # Green
    elif bright >= 0.30:
        freq, color = E4, (1, 1, 0)   # Yellow
    elif bright >= 0.20:
        freq, color = D4, (1, 1, 0)   # Yellow
    elif bright >= 0.10:
        freq, color = C4, (1, 0, 0)   # Red
    else:
        freq, color = C4, (1, 0, 0)   # Red

    buzzer_pin.freq(freq)
    buzzer_pin.duty_u16(1000)  # Low volume
    show(*color)

    print(f"raw={smoothed} bright={bright:.2f} freq={freq} color={color}")

# --- Web Server ---
async def handle_request(reader, writer):
    """Handles incoming HTTP requests."""
    global api_note_task

    print("Client connected")
    request_line = await reader.readline()
    while await reader.readline() != b"\r\n":
        pass

    try:
        request = str(request_line, "utf-8")
        method, url, _ = request.split()
        print(f"Request: {method} {url}")
    except (ValueError, IndexError):
        writer.write(b"HTTP/1.0 400 Bad Request\r\n\r\n")
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return

    light_value = photo_sensor.read_u16()
    response = ""
    content_type = "text/html"

    if method == "GET" and url == "/":
        html = f"""
        <html>
            <body>
                <h1>Pico Light Orchestra</h1>
                <p>Current light sensor reading: {light_value}</p>
            </body>
        </html>
        """
        response = html
    elif method == "POST" and url == "/play_note":
        raw_data = await reader.read(1024)
        try:
            data = json.loads(raw_data)
            freq = data.get("frequency", 0)
            duration = data.get("duration", 0)

            if api_note_task:
                api_note_task.cancel()

            api_note_task = asyncio.create_task(play_api_note(freq, duration))

            response = '{"status": "ok", "message": "Note playing started."}'
            content_type = "application/json"
        except (ValueError, json.JSONDecodeError):
            writer.write(b'HTTP/1.0 400 Bad Request\r\n\r\n{"error": "Invalid JSON"}\r\n')
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return
    elif method == "POST" and url == "/stop":
        if api_note_task:
            api_note_task.cancel()
            api_note_task = None
        stop_tone()
        response = '{"status": "ok", "message": "All sounds stopped."}'
        content_type = "application/json"
    else:
        writer.write(b"HTTP/1.0 404 Not Found\r\n\r\n")
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return

    writer.write(
        f"HTTP/1.0 200 OK\r\nContent-type: {content_type}\r\n\r\n".encode("utf-8")
    )
    writer.write(response.encode("utf-8"))
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    print("Client disconnected")

# --- Main Loop ---
async def main():
    global api_note_task
    try:
        ip = connect_to_wifi()
        print(f"Starting web server on {ip}...")
        asyncio.create_task(asyncio.start_server(handle_request, "0.0.0.0", 80))
    except Exception as e:
        print(f"Failed to initialize: {e}")
        return

    while True:
        if not api_note_task or api_note_task.done():
            light_to_tone_and_led()
        await asyncio.sleep_ms(200)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program stopped.")
        stop_tone()
        show(0, 0, 0)
