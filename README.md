# Micropython low power support workaround for Rasberry Pico

It seems the current port of micropython for the Raspberry Pico does not yet fully support low power sleep (see for example [this issue](https://github.com/micropython/micropython/issues/7035)).

This repository contains experimental code aiming at adding ad-hoc support using the pico facilities. To use it, simply copy the `lowpower.py` library on you pico and `import lowpower` in your program.

## NOTICE

This project is extremely **experimental**, and not production-tested. No guaranty is provided, so use at your own risks.

If your Pico seems to be stuck in sleep mode, unpowering and repowering it should solve the issue.

## Features

The following functions are implemented:

### Dormant mode

``` python
dormant_until_pin(GPIO_PIN_NUMBER)
```

Use Pico "DORMANT" mode to enter deep sleep until receiving a signal on the given GPIO pin number. This mode greatly reduces energy consumption of the Pico.

Note that except if you know what you're doing, you should abstain to configure the Pin used for the dormant mode for other uses.

Example:

``` python
import lowpower

DORMANT_PIN = 15

print("before dormant")
lowpower.dormant_until_pin(DORMANT_PIN)
print("after dormant") # only print after receiving signal on Pin number DORMANT_PIN
```

You can also sleep on multiple pins using `dormant_until_pins`

Example:

``` python
import lowpower

DORMANT_PIN1 = 16
DORMANT_PIN2 = 17

print("before dormant")
lowpower.dormant_until_pins([DORMANT_PIN1, DORMANT_PIN2])
print("after dormant") # only print after receiving signal on one of the pins
```

The lower-level `dormant_with_modes` allows to set different wake-up conditions for each individual pin.

For convenience, `lowpower` exposes the four possibles wake-up conditions as the constants `EDGE_LOW`, `EDGE_HIGH`, `LEVEL_LOW` and `LEVEL_HIGH`.

Example:
``` python
import lowpower

DORMANT_PIN1 = 16
DORMANT_PIN2 = 17

print("before dormant")
lowpower.dormant_with_modes({
        DORMANT_PIN1: (lowpower.EDGE_LOW | lowpower.EDGE_HIGH),
        DORMANT_PIN2: lowpower.LEVEL_HIGH,
})
print("after dormant") # only print after receiving the correct signal on one of the pins
```

### Lightsleep mode

``` python
lightsleep()
```

Set the pico to wait on a signal on any GPIO. This mode should moderately reduce energy consumption of the Pico (but is still subject to improvements at this stage).


Example:

``` python
from machine import Pin
import lowpower

DORMANT_PIN = 15

btn = Pin(DORMANT_PIN, Pin.IN, Pin.PULL_DOWN)
btn.irq(lambda e: print("button event!"),
        Pin.IRQ_RISING)

print("before lightsleep")
lowpower.lightsleep()
print("after lightsleep") # only print after receiving signal on any GPIO pin
```

## Power consumption

Here are some experimental measurements of the pico current "consumption" under different regimes. You can reproduce these results using the `lowpower_example.py` (and a multimeter :smile:).

| Regime      | Current (mA) |
| ----------- | -----------: |
| Active loop |          26  |
| Sleep       |          22  |
| Lightsleep  |          22  |
| Dormant     |           1  |

## License

This project and all its files are licensed under the LGPLv3.

The TL;DR version of the LGPL (and my intent) is that you can freely use this code in your project (be it Free software, open-source or closed-source) as long as:
- you mention this project and a way to get it (a link to this repository will do)
- you do not modify the code of this project

If however you want to modify the code of this project, then you must either:
- redistribute it under LGPL yourself
- contribute it back to this project so that I (and anyone :) ) can benefit from your improvement

See the file `LICENSE.txt` and [https://www.gnu.org/licenses/lgpl-3.0.html](https://www.gnu.org/licenses/lgpl-3.0.html) for more information.

In case you want to use this project but have an issue regarding the licence, feel free to contact me to see if we can work something out :smile:
