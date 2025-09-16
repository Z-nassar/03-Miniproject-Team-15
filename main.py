from machine import Pin, PWM, ADC
import time

# -------- Pins --------
ADC1_PIN  = 28      # photodiode 1 -> GP28 (ADC2)
ADC2_PIN  = 27      # photodiode 2 -> GP27 (ADC1)
BUZZ_PIN  = 15      # buzzer (PWM)
R_PIN     = 1       # RGB LED pins
G_PIN     = 2
B_PIN     = 3

# -------- Buzzer / LED configuration --------
TONE_FREQ  = 523         # same note
VOL_LOUD   = 5000
VOL_MED    = 1000
VOL_QUIET  = 500

# LED helpers
R = Pin(R_PIN, Pin.OUT)
G = Pin(G_PIN, Pin.OUT)
B = Pin(B_PIN, Pin.OUT)
def show(r, g, b):
    R.value(1 if r else 0)
    G.value(1 if g else 0)
    B.value(1 if b else 0)

buzzer = PWM(Pin(BUZZ_PIN))
buzzer.freq(TONE_FREQ)
buzzer.duty_u16(0)

# Two ADC channels
ldr1 = ADC(ADC1_PIN)
ldr2 = ADC(ADC2_PIN)

# Smoothing to reduce jitter (one filter per sensor)
alpha = 0.2
sm1 = ldr1.read_u16()
sm2 = ldr2.read_u16()

def to_brightness(raw_u16: int) -> float:
    # With 10k->3V3 (top) and LDR->GND (bottom), more light => lower voltage.
    # Map to 0..1 where 1 = bright
    b = 1.0 - (raw_u16 / 65535.0)
    if b < 0: b = 0.0
    if b > 1: b = 1.0
    return b

print("Reading two photoresistors... (shine light on each and watch)")
try:
    while True:
        # Read & smooth
        r1 = ldr1.read_u16()
        r2 = ldr2.read_u16()
        sm1 = int(alpha * r1 + (1 - alpha) * sm1)
        sm2 = int(alpha * r2 + (1 - alpha) * sm2)

        b1 = to_brightness(sm1)
        b2 = to_brightness(sm2)

        # Combine the two sensors:
        combined = max(b1, b2)

        # Thresholds
        if combined >= 0.92:
            band = "BRIGHT (LOUD)"
            duty = VOL_LOUD
            show(1, 0, 0)          # RED
        elif combined >= 0.35:
            band = "MEDIUM"
            duty = VOL_MED
            show(0, 1, 0)          # GREEN
        else:
            band = "LOW"
            duty = VOL_QUIET
            show(0, 0, 1)          # BLUE

        buzzer.duty_u16(duty)

        # Debug print
        print(
            f"LDR1 raw={sm1:5d} b1={b1:.2f} | "
            f"LDR2 raw={sm2:5d} b2={b2:.2f} | "
            f"combined={combined:.2f} -> {band}, duty={duty}"
        )

        time.sleep(0.1)

except KeyboardInterrupt:
    buzzer.duty_u16(0)
    show(0, 0, 0)
