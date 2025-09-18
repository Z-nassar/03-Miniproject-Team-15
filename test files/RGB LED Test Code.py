from machine import Pin
import time

# RGB LED pins (non-ADC). Each color has 220 ohms.
R_PIN = 1
G_PIN = 2
B_PIN = 3

# Configure the three GPIOs as outputs (one per color).
R = Pin(R_PIN, Pin.OUT)
G = Pin(G_PIN, Pin.OUT)
B = Pin(B_PIN, Pin.OUT)

# If your LED is common-cathode, leave True (1 = ON, 0 = OFF).
# If it's common-anode, set to False (logic inverted: 0 = ON, 1 = OFF).
ACTIVE_HIGH = True

def color_write(pin: Pin, on: bool) -> None:
#Drive a single LED channel with the correct polarity.
    pin.value(1 if (on == ACTIVE_HIGH) else 0)

def show(r: bool, g: bool, b: bool) -> None:
 # Set the LED color using booleans for Red/Green/Blue
    color_write(R, r)
    color_write(G, g)
    color_write(B, b)

def alternate_colors(delay_s: float = 2.0) -> None:
#Alternate Blue → Green → Red, printing the color and holding each for delay_s seconds.
    while True:
        show(0, 0, 1)   # Blue only
        print("Blue")
        time.sleep(delay_s)

        show(0, 1, 0)   # Green only
        print("Green")
        time.sleep(delay_s)

        show(1, 0, 0)   # Red only
        print("Red")
        time.sleep(delay_s)

# Run the alternating-color loop.
alternate_colors()
