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

See the file `LICENSE.txt` and [https://www.gnu.org/licenses/lgpl-3.0.html](https://www.gnu.org/licenses/lgpl-3.0.html) for more information.
