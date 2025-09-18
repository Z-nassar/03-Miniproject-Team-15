from machine import Pin, PWM, ADC
import time

# ----- Pins -----
ADC1_PIN   = 28      # photoresistor 1 -> GP28 / ADC2
ADC2_PIN   = 27      # photoresistor 2 -> GP27 / ADC1
BUZZER_PIN = 15      # buzzer GP15 with PWM
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

# ----- Two photoresistors (ADC) -----
ldr1 = ADC(ADC1_PIN)
ldr2 = ADC(ADC2_PIN)
alpha = 0.2                      # smoothing factor
sm1 = ldr1.read_u16()            # seeds for EMA
sm2 = ldr2.read_u16()

def to_brightness(raw_u16: int) -> float:
    # More light = lower voltage with this divider, so invert.
    b = 1.0 - (raw_u16 / 65535.0)
    if b < 0: b = 0.0
    if b > 1: b = 1.0
    return b

print("Reading two photoresistors... cover/uncover to see changes.")
try:
    while True:
        # Read & smooth both sensors
        r1 = ldr1.read_u16()
        r2 = ldr2.read_u16()
        sm1 = int(alpha * r1 + (1 - alpha) * sm1)
        sm2 = int(alpha * r2 + (1 - alpha) * sm2)

        b1 = to_brightness(sm1)
        b2 = to_brightness(sm2)
        bmax = b1 if b1 >= b2 else b2

        pct1 = int(b1 * 100)
        pct2 = int(b2 * 100)
        pct_max = int(bmax * 100)

        # Thresholds for color and volume (same as before, applied to MAX brightness)
        if bmax >= 0.85:
            color, vol_name, duty = "red", "loud", VOL_LOUD
            show(1, 0, 0)
        elif bmax >= 0.50:
            color, vol_name, duty = "green", "medium", VOL_MED
            show(0, 1, 0)
        else:
            color, vol_name, duty = "blue", "quiet", VOL_QUIET
            show(0, 0, 1)

        buzzer.duty_u16(duty)

        # Print requested message
        print(f"max brightness {pct_max:3d}% (PR1: {pct1:3d}%, PR2: {pct2:3d}%), "
              f"{color} LED, {vol_name} volume")

        time.sleep(0.1)

except KeyboardInterrupt:
    buzzer.duty_u16(0)
    show(0, 0, 0)
