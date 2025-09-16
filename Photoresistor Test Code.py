from machine import ADC, Pin
import time

# Photoresistor/photodiode on GP28 (ADC2)
SENSOR_PIN = 28
sensor = ADC(Pin(SENSOR_PIN))

# Jitter smoothing (0..1), higher = smoother/slower
alpha = 0.2
sm = sensor.read_u16()

# more light means less voltage so we invert it to make brightness increase with light
INVERT = True

def to_brightness(raw_u16: int) -> float:
    x = raw_u16 / 65535.0
    b = (1.0 - x) if INVERT else x
    return 0.0 if b < 0 else (1.0 if b > 1 else b)

print("Reading light level on GP28 (ADC2).")
try:
    while True:
        raw = sensor.read_u16()
        sm = int(alpha * raw + (1 - alpha) * sm)
        bright = to_brightness(sm)
        pct = int(bright * 100)  # 0..100%
        print(f"brightness={pct:3d}%")
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
