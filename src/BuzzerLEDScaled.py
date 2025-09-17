from machine import Pin, PWM, ADC
import time

# -------- Pins --------
ADC_PIN   = 28      # photoresistor node (GP28 / ADC2)
BUZZ_PIN  = 15      # passive piezo buzzer (PWM)
R_PIN     = 1       # RGB LED pins (non-ADC)
G_PIN     = 2
B_PIN     = 3

# -------- Buzzer config --------
C4 = 262
D4 = 294
E4 = 330
F4 = 349
G4 = 392
A4 = 440
B4 = 494
C5 = 523

# LED helpers (common-cathode; invert if common-anode)
R = Pin(R_PIN, Pin.OUT)
G = Pin(G_PIN, Pin.OUT)
B = Pin(B_PIN, Pin.OUT)
def show(r, g, b):
    R.value(1 if r else 0)
    G.value(1 if g else 0)
    B.value(1 if b else 0)

buzzer = PWM(Pin(BUZZ_PIN))
buzzer.freq(C4)
buzzer.duty_u16(1000)

ldr = ADC(ADC_PIN)

# Smoothing to reduce jitter
alpha = 0.2
smoothed = ldr.read_u16()

print("Reading photoresistor... (cover/uncover it and watch output)")
try:
    while True:
        raw = ldr.read_u16()                 # 0..65535
        smoothed = int(alpha*raw + (1-alpha)*smoothed)

        # With 10k->3V3 (top) and LDR->GND (bottom), more light => lower voltage.
        # Map so 'bright' increases with light.
        bright = 1.0 - (smoothed / 65535.0)
        if bright < 0: bright = 0.0
        if bright > 1: bright = 1.0

        # ---- Thresholds ----
        if bright >= 0.90:
            buzzer.freq(C5)
            show(1, 0, 0)     # Red
            color = "Red"
        elif bright >= 0.80:
            buzzer.freq(C5)
            show(1, 0, 0)     # Red
            color = "Red"
        elif bright >= 0.70:
            buzzer.freq(B4)
            show(1, 0, 1)     # Purple
            color = "Purple"
        elif bright >= 0.60:
            buzzer.freq(A4)
            show(0, 0, 1)     # Blue
            color = "Blue"
        elif bright >= 0.50:
            buzzer.freq(G4)
            show(0, 0, 1)     # Blue
            color = "Blue"
        elif bright >= 0.40:
            buzzer.freq(F4)
            show(0, 1, 0)     # Green
            color = "Green"
        elif bright >= 0.30:
            buzzer.freq(E4)
            show(1, 1, 0)     # Yellow
            color = "Yellow"
        elif bright >= 0.20:
            buzzer.freq(D4)
            show(1, 1, 0)     # Yellow
            color = "Yellow"
        elif bright >= 0.10:
            buzzer.freq(C4)
            show(1, 0, 0)     # Red
            color = "Red"
        else:
            buzzer.freq(C4)
            show(1, 0, 0)     # Red
            color = "Red"
        
        buzzer.duty_u16(1000)   # Medium Volume in other versions

        # Debug print
        print(f"raw={smoothed:5d}  bright={bright:.2f}  color = {color}")
        
        time.sleep(0.2)         # Changes time between tone/color updates

except KeyboardInterrupt:
    buzzer.duty_u16(0)
    show(0, 0, 0)
