from machine import Pin, PWM
import time

# Buzzer configuration
BUZZER_PIN = 15
TONE_FREQ  = 523  # C5

# Volume levels 
VOL_LOUD   = 5000
VOL_MED    = 1000
VOL_QUIET  = 500

# Initializing buzzer
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.freq(TONE_FREQ)
buzzer.duty_u16(0)

levels = [("QUIET", VOL_QUIET), ("MEDIUM", VOL_MED), ("LOUD", VOL_LOUD)]

try:
    while True:
        for name, duty in levels:
            buzzer.duty_u16(duty)   # same note, new volume
            print(f"Volume: {name}  duty={duty}")
            time.sleep(2)           # hold each volume for 2 seconds

except KeyboardInterrupt:
    buzzer.duty_u16(0)             