# 2025 Fall ECE Senior Design Miniproject

[Project definition](./Project.md)

This project uses the Raspberry Pi Pico 2WH SC1634 (wireless, with header pins).

Each team must provide a micro-USB cable that connects to their laptop to plug into the Pi Pico.
The cord must have the data pins connected.
Splitter cords with multiple types of connectors fanning out may not have data pins connected.
Such micro-USB cords can be found locally at Microcenter, convenience stores, etc.
The student laptop is used to program the Pi Pico.
The laptop software to program and debug the Pi Pico works on macOS, Windows, and Linux.

This miniproject focuses on using
[MicroPython](./doc/micropython.md)
using
[Thonny IDE](./doc/thonny.md).
Other IDE can be used, including Visual Studio Code or
[rshell](./doc/rshell.md).

## Hardware
* Raspberry Pi Pico WH [SC1634](https://pip.raspberrypi.com/categories/1088-raspberry-pi-pico-2-w) (WiFi, Bluetooth, with header pins)
* Freenove Pico breakout board [FNK0081](https://store.freenove.com/products/fnk0081)
* Piezo Buzzer SameSky [CPT-3095C-300](https://www.mouser.com/datasheet/3/6118/1/cpt-3095c-300.pdf)
* Photoresistor Advanced Photonix [NSL-A5013](https://www.mouser.com/datasheet/3/5923/1/ds-nsl-a501-series.pdf) 
* Three 220 ohm resistors
* One 10k ohm resistor

### Circuit/Hardware Configuration (Zachary Nassar)
<img width="804" height="758" alt="image" src="https://github.com/user-attachments/assets/fbaa90a9-11e3-4ad3-829e-cc4682dff288" />

The above figure represents a flattened ideal view of the circuit configuration that was used for our project. Unfortunately, the software used to create the image (TinkerCAD) does not have the ability to represent a Raspberry Pi Pico 2 W. So, instead an Arduino Uno board was used as a stand-in. Other parts that were used in this configuration included three 220 ohm resistors, one 30 kohm resistor, a buzzer, an RGB LED, and a photoresistor. The three 220 ohm resistors were connected to the positive leads of the RGB LED while the 30 kohm resistor was used in series with the photoresistor.


### Component Test Codes (Ezan Khan)
I wired the circuit together and coded test files for all our components. Some of the files I added are:
1. Buzzer Test Code.py — PWM buzzer on GP15 at 523 Hz; cycles quiet → medium → loud every 2 seconds and prints the volume level.
2. RGB LED Test Code.py — RGB LED on GP1/GP2/GP3; cycles blue → green → red every 2 seconds and prints the color.
3. Photoresistor Test Code.py — Reads LDR on GP28 (ADC2), smooths it, inverts it, reads and prints 0–100% brightness from photoresistor every 0.1 second.
4. Buzzer LED Test Code.py — Maps buzzer and LED together such that it cycles blue/quiet → green/medium → red/loud every 2 seconds.
5. main v2.py — Maps brightness on photoresistors to output on the buzzer and LED such that low brightness is blue + quiet, medium brightness is green + medium, high brightness is red + loud. Thresholds are reached by taking the max brightness out of both photoresistors to cover more surface area.

[Watch the demo video](media/light%20orchestra%20recording.mov)


### CAD Enclosure (Keimaree Smith)
My task was to make a mock enclosure for the device that's built to scale, should we decide to print this professional housing for our final product. The measurements are as follows:
Measurements:(LxWxH)

Raspberry Pi=63mm x 57mm x 23mm

Buzzer speaker=29.7mm x 29.7mm x 9.2mm

Switches=12mm x 12mm x 7.3mm 

Led=5.8mm x 5.8mm x 9mm

Photoresistor= 5.8mm x 5.8mm x 5.5mm
<img width="1898" height="1084" alt="image" src="https://github.com/user-attachments/assets/d711d2e8-3b7f-4784-a469-68182a312c6b" />
<img width="1898" height="1094" alt="image" src="https://github.com/user-attachments/assets/a0cd9500-33db-46f3-b81e-2906e4b059a7" />

# Should the two following sections be removed?

### Photoresistor details

The photoresistor uses the 10k ohm resistor as a voltage divider
[circuit](./doc/photoresistor.md).
The 10k ohm resistor connects to "3V3" and to ADC2.
The photoresistor connects to the ADC2 and to AGND.
Polarity is not important for this resistor and photoresistor.

The MicroPython
[machine.ADC](https://docs.micropython.org/en/latest/library/machine.ADC.html)
class is used to read the analog voltage from the photoresistor.
The `machine.ADC(id)` value corresponds to the "GP" pin number.
On the Pico W, GP28 is ADC2, accessed with `machine.ADC(28)`.

### Piezo buzzer details

PWM (Pulse Width Modulation) can be used to generate analog signals from digital outputs.
The Raspberry Pi Pico has eight PWM groups each with two PWM channels.
The [Pico WH pinout diagram](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf)
shows that almost all Pico pins can be used for multiple distinct tasks as configured by MicroPython code or other software.
In this exercise, we will generate a PWM signal to drive a speaker.

GP16 is one of the pins that can be used to generate PWM signals.
Connect the speaker with the black wire (negative) to GND and the red wire (positive) to GP16.

In a more complete project, we would use additional resistors and capacitors with an amplifer to boost the sound output to a louder level with a bigger speaker.
The sound output is quiet but usable for this exercise.

Musical notes correspond to particular base frequencies and typically have rich harmonics in typical musical instruments.
An example soundboard showing note frequencies is [clickable](https://muted.io/note-frequencies/).
Over human history, the corresspondance of notes to frequencies has changed over time and location and musical cultures.
For the question below, feel free to use musical scale of your choice!

[Music Examples](https://github.com/twisst/Music-for-Raspberry-Pi-Pico/blob/main/play.py)
## Raspberry Pi Pico 2W API Integration (John Goytia, Prashast Pandey)

This project demonstrates how to integrate an API with the Raspberry Pi Pico 2W to enable remote interaction over Wi-Fi.  
The Pico 2W is programmed to connect to a wireless network, making it accessible to other devices on the same network.  
A student computer can send HTTP API requests (both GET and POST) to the Pico, allowing for real-time control and data retrieval.

## Features
- **Play a Tune**  
  The Pico can generate and play a tune through its connected buzzer.  
  - `GET /play-tune` will play a default tune.  
  - `POST /play-tune` can include parameters (e.g., note or duration) to customize the sound.

- **Light Intensity Measurement**  
  The Pico is equipped with a light sensor to measure surrounding light levels.  
  - `GET /light-intensity` will return the current sensor reading.  
  - `POST /light-intensity` can log or trigger further actions with the sensor value.

## Project Overview
This setup demonstrates how microcontrollers like the Raspberry Pi Pico 2W can be used in IoT applications,  
where devices respond to remote commands or provide sensor data over a network.

By combining API requests (GET and POST) with wireless communication, this project provides a simple but effective model  
for building interactive IoT systems that bridge hardware with network-based control.


## GET request to play a default tune
curl http://<PICO_IP>/play-tune

## POST request to play a tune with parameters
curl -X POST http://<PICO_IP>/play-tune -d '{"note":"C","duration":2}'

## GET request to read light intensity
curl http://<PICO_IP>/light-intensity

## POST request with light intensity data (example use case)
curl -X POST http://<PICO_IP>/light-intensity -d '{"action":"log"}'

# Should the two following sections be removed?

## Notes

Pico MicroPython time.sleep() doesn't error for negative values even though such are obviously incorrect--it is undefined for a system to sleep for negative time.
Duty cycle greater than 1 is undefined, so we clip the duty cycle to the range [0, 1].


## Reference

* [Pico 2WH pinout diagram](https://datasheets.raspberrypi.com/picow/pico-2-w-pinout.pdf) shows the connections to analog and digital IO.
* Getting Started with Pi Pico [book](https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf)
