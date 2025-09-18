from machine import Pin, PWM, ADC
import time

# ----- Pins -----
ADC_PIN   = 28      # photoresistor GP28 / ADC2
BUZZER_PIN = 15     # buzzer GP15 with PWM
R_PIN = 1            # Red pin GP1
G_PIN = 2            # Green pin GP2
B_PIN = 3            # Blue pin GP3

# ----- Audio -----
TONE_FREQ  = 523    # Note C5
VOL_LOUD   = 5000
VOL_MED    = 1000
VOL_QUIET  = 500

# ----- LED setup -----
R = Pin(R_PIN, Pin.OUT)
G = Pin(G_PIN, Pin.OUT)
B = Pin(B_PIN, Pin.OUT)
def show(r, g, b):
    R.value(1 if r else 0)
    G.value(1 if g else 0)
    B.value(1 if b else 0)

# ----- Buzzer setup -----
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.freq(TONE_FREQ)
buzzer.duty_u16(0)

# ----- Photoresistor (ADC) -----
ldr = ADC(ADC_PIN)
alpha = 0.2                         # smoothing factor
smoothed = ldr.read_u16()           # seed

print("Reading photoresistor... cover/uncover to see changes.")
try:
    while True:
        raw = ldr.read_u16()                             # 0..65535
        smoothed = int(alpha*raw + (1-alpha)*smoothed)

        # More light = lower voltage.
        # Invert so bright increases with light
        bright = 1.0 - (smoothed / 65535.0)
        if bright < 0: bright = 0.0
        if bright > 1: bright = 1.0
        pct = int(bright * 100)

        # Thresholds for color and volume
        if bright >= 0.85:
            color, vol_name, duty = "red", "loud", VOL_LOUD
            show(1, 0, 0)
        elif bright >= 0.50:
            color, vol_name, duty = "green", "medium", VOL_MED
            show(0, 1, 0)
        else:
            color, vol_name, duty = "blue", "quiet", VOL_QUIET
            show(0, 0, 1)

        buzzer.duty_u16(duty)
        print(f"brightness of {pct:3d}% so we have a {color} LED and {vol_name} volume")

        time.sleep(0.1)

except KeyboardInterrupt:
    buzzer.duty_u16(0)
    show(0, 0, 0)
