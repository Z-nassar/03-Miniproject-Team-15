# 2025 Fall ECE Senior Design Miniproject

[Project definition](./Project.md)

The goal of this project was to use the provided Raspberry Pi Pico 2WH SC1634 (wireless, with header pins), buzzer, and photoresistor to create a light ochestra (a device that would produce a sound or other output as a result of a light input). Several different lines of development were followed in this project and the result was four distinct deliverables: API intergration for the Raspberry Pi, a light orchestra with two photoresistors that scales volume, a light orchestra with one photoresistor that scales tone (derived from the volume light orchestra), and a CAD model of a possible enclosure for the device. 

This project used [MicroPython](./doc/micropython.md) and [Thonny IDE](./doc/thonny.md).

## Videos/Demoes
* [Working with API](https://drive.google.com/file/d/1rF_9OHENMlV6wJc0hUqTYPZZ5KIkNX32/view?usp=sharing)
* [Light Orchestra with Photoresistors, LED, Buzzer](https://drive.google.com/file/d/1zt_kSiG6cxKfdzKx5vofzYIg05cQD7c7/view?usp=sharing)
* [Light Orchestra with a Scaled Tone Output](https://drive.google.com/file/d/1YlJdYv4P6-w5sr-QGmZmXdrBWFg7n6NT/view?usp=sharing)

## Hardware
* Raspberry Pi Pico WH [SC1634](https://pip.raspberrypi.com/categories/1088-raspberry-pi-pico-2-w) (WiFi, Bluetooth, with header pins)
* Freenove Pico breakout board [FNK0081](https://store.freenove.com/products/fnk0081)
* Piezo Buzzer SameSky [CPT-3095C-300](https://www.mouser.com/datasheet/3/6118/1/cpt-3095c-300.pdf)
* Two Photoresistor Advanced Photonix [NSL-A5013](https://www.mouser.com/datasheet/3/5923/1/ds-nsl-a501-series.pdf) 
* Three 220 Ohm Resistors
* Two 10k Ohm Resistor
* One 30k Ohm Resistor
* One RGB LED

## Circuit/Hardware Configuration
<img width="620" height="606" alt="image" src="https://github.com/user-attachments/assets/69597318-c87e-44b7-86c0-0a5f9d715e4f" />

The above figure represents a flattened ideal view of the first circuit configuration that was used for our project. Unfortunately, the software used to create the image (TinkerCAD) does not have the ability to represent a Raspberry Pi Pico 2 W. So, instead an Arduino Uno board was used as a stand-in. Other parts that were used in this configuration included three 220 ohm resistors, two 10k ohm resistor, a buzzer, an RGB LED, and two photoresistors. The three 220 ohm resistors were connected to the positive leads of the RGB LED while the two 10 kohm resistors were used in series with the photoresistors.

<img width="278" height="464" alt="image" src="https://github.com/user-attachments/assets/484a663a-cb8a-42c5-b1c2-f667f36ec40b" />

The above figure is an image of the first circuit configuration that was used for our project.



<img width="804" height="758" alt="image" src="https://github.com/user-attachments/assets/fbaa90a9-11e3-4ad3-829e-cc4682dff288" />

The above figure represents a flattened ideal view of the second circuit configuration that was used for our project. Again, the Arduino Uno was used as a stand-in for a Raspberry Pi Pico. Other parts that were used in this configuration included three 220 ohm resistors, one 30k oohm resistor, a buzzer, an RGB LED, and a photoresistor. The three 220 ohm resistors were connected to the positive leads of the RGB LED while the 30 kohm resistor was used in series with the photoresistor.

<img width="512" height="849" alt="image" src="https://github.com/user-attachments/assets/e529e0e4-d308-46e1-b3a8-458d82a88e45" />

The above figure is an image of the second circuit configuration that was used for our project.


## Component Test Codes (Ezan Khan)
I wired the circuit together and coded test files for all our components. Some of the files I added are:
1. Buzzer Test Code.py — PWM buzzer on GP15 at 523 Hz; cycles quiet → medium → loud every 2 seconds and prints the volume level.
2. RGB LED Test Code.py — RGB LED on GP1/GP2/GP3; cycles blue → green → red every 2 seconds and prints the color.
3. Photoresistor Test Code.py — Reads LDR on GP28 (ADC2), smooths it, inverts it, reads and prints 0–100% brightness from photoresistor every 0.1 second.
4. Buzzer LED Test Code.py — Maps buzzer and LED together such that it cycles blue/quiet → green/medium → red/loud every 2 seconds.
5. main v2.py — Maps brightness on photoresistors to output on the buzzer and LED such that low brightness is blue + quiet, medium brightness is green + medium, high brightness is red + loud. Thresholds are reached by taking the max brightness out of both photoresistors to cover more surface area.

Watch the [demo video](light%20orchestra%20recording.mov). If that link doesn't work, try [this](https://drive.google.com/file/d/1zt_kSiG6cxKfdzKx5vofzYIg05cQD7c7/view?usp=sharing).


## CAD Enclosure (Keimaree Smith)
Online 3D viewing for product housing: https://a360.co/47LtF9N

My task was to make a mock enclosure for the device that's built to scale, should we decide to print this professional housing for our final product. The measurements are as follows:
Measurements:(LxWxH)
* Raspberry Pi=63mm x 57mm x 23mm
* Buzzer speaker=29.7mm x 29.7mm x 9.2mm
* Switches=12mm x 12mm x 7.3mm
* Led=5.8mm x 5.8mm x 9mm
* Photoresistor= 5.8mm x 5.8mm x 5.5mm
<img width="1898" height="1084" alt="image" src="https://github.com/user-attachments/assets/d711d2e8-3b7f-4784-a469-68182a312c6b" />
<img width="1898" height="1094" alt="image" src="https://github.com/user-attachments/assets/a0cd9500-33db-46f3-b81e-2906e4b059a7" />

## Raspberry Pi Pico 2W API Integration (John Goytia, Prashast Pandey)

This project demonstrates how to integrate an API with the Raspberry Pi Pico 2W to enable remote interaction over Wi-Fi.  
The Pico 2W is programmed to connect to a wireless network, making it accessible to other devices on the same network.  
A student computer can send HTTP API requests (both GET and POST) to the Pico, allowing for real-time control and data retrieval.

#### Features
- **Play a Tune**  
  The Pico can generate and play a tune through its connected buzzer.  
  - `GET /play-tune` will play a default tune.  
  - `POST /play-tune` can include parameters (e.g., note or duration) to customize the sound.

- **Light Intensity Measurement**  
  The Pico is equipped with a light sensor to measure surrounding light levels.  
  - `GET /light-intensity` will return the current sensor reading.  
  - `POST /light-intensity` can log or trigger further actions with the sensor value.

#### Project Overview
This setup demonstrates how microcontrollers like the Raspberry Pi Pico 2W can be used in IoT applications,  
where devices respond to remote commands or provide sensor data over a network.

By combining API requests (GET and POST) with wireless communication, this project provides a simple but effective model  
for building interactive IoT systems that bridge hardware with network-based control.


#### GET request to play a default tune
curl http://<PICO_IP>/play-tune

#### POST request to play a tune with parameters
curl -X POST http://<PICO_IP>/play-tune -d '{"note":"C","duration":2}'

#### GET request to read light intensity
curl http://<PICO_IP>/light-intensity

#### POST request with light intensity data (example use case)
curl -X POST http://<PICO_IP>/light-intensity -d '{"action":"log"}'


## Feature Extension and Documentation (Zachary Nassar)
I expanded on the mainv2.py code written by Ezan such that light intensity was mapped to a scale of tones instead of volume. Additionally, I changed the behaviour of the LED so that it would flash through a scale of colors as light intensity increased. This can be seen in the file BuzzerLEDScaled.py.

I also generally updated the README and created the TinkerCAD figures of the circuit configurations used in our project.


## Next Steps
If more time was allocated to work on this project, some next steps we would take would be to:
* Integrate the the light orchestra code and the API integration code as well as to integrate the two different versions of the light orchestra code
* Add the ability to change the octave of the scale for the scaled tones light orchestra

## Reference
* [Pico 2WH pinout diagram](https://datasheets.raspberrypi.com/picow/pico-2-w-pinout.pdf) shows the connections to analog and digital IO.
* Getting Started with Pi Pico [book](https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf)
* [TinkerCAD](https://www.tinkercad.com/)
