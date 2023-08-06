# rpi-gpio-devices

Control Raspberry Pi gpio pins more easily.

This module provides an abstraction layer to control connected devices
(fans, switches, LEDs, buttons) more easily with ready to use device classes and functions.

It uses the [RPi.GPIO](https://pypi.org/project/RPi.GPIO) module to control the GPIO pins.
Currently this is the recommended module to use for archlinuxarm, but it only provides
basic functions to manipulate the pins.

## Installation

`pip install rpi-gpio-devices`

[pypi](https://pypi.org/project/rpi-gpio-devices)

## Few examples

#### Automatic fan control based on CPU temp
``` py
from time import sleep

from rpi_gpio_devices import Fan

# Basic usage
pwm_fan = Fan(power=29, sense=35, pwm=33)

try:
    while True:
        pwm_fan.auto_set()
except KeyboardInterrupt:
    pwm_fan.cleanup()
```

#### Set LED brightness with PWM
``` py
from time import sleep

from rpi_gpio_devices import PWMLED

pwmled = PWMLED(33)

pwmled.set_brightness(50)
sleep(2)
pwmled.set_brightness(100)
sleep(2)
pwmled.set_brightness(0)
# pwmled.turn_off() # Or simply just turn it off

pwmled.cleanup()
```

#### Check if a button is pressed
``` py
from time import sleep

from rpi_gpio_devices import Button

button = Button(11)

try:
    while True:
        if button.is_pressed():
            print('Button is pressed!')
        sleep(0.5)
except KeyboardInterrupt:
    button.cleanup()
```

More in the [examples](https://github.com/danieltodor/rpi-gpio-devices/tree/master/examples)
directory.
