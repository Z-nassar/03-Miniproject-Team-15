from machine import Pin, PWM
import time

# ----- Pins -----
BUZZER_PIN = 15      # buzzer with PWM
R_PIN = 1            # Red pin
G_PIN = 2            # Green pin
B_PIN = 3            # Blue pin

# ----- Audio -----
TONE_FREQ  = 523     # Note C5
VOL_LOUD   = 5000
VOL_MED    = 1000
VOL_QUIET  = 500

# ----- LED setup -----
ACTIVE_HIGH = True   # False if common-anode (logic inverted)

R = Pin(R_PIN, Pin.OUT)
G = Pin(G_PIN, Pin.OUT)
B = Pin(B_PIN, Pin.OUT)

def _write(pin, on):
    pin.value(1 if (on == ACTIVE_HIGH) else 0)

def show(r, g, b):
    _write(R, r)
    _write(G, g)
    _write(B, b)

# ----- Buzzer setup -----
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.freq(TONE_FREQ)
buzzer.duty_u16(0)

# Sequence order of color_name, volume_name, (R,G,B), duty
sequence = [
    ("Blue",  "quiet",  (0, 0, 1), VOL_QUIET),
    ("Green", "medium", (0, 1, 0), VOL_MED),
    ("Red",   "loud",   (1, 0, 0), VOL_LOUD),
]

try:
    while True:
        for color, vol_name, (r, g, b), duty in sequence:
            show(r, g, b)
            buzzer.duty_u16(duty)
            print(f"{color} LED and {vol_name} volume")
            time.sleep(2)

except KeyboardInterrupt:
    buzzer.duty_u16(0)
    show(0, 0, 0)
