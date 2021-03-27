from machine import Pin
from time import sleep_ms

import lowpower

LED_BUSY = 25
busy_led = Pin(LED_BUSY, Pin.OUT)

busy_led.value(1)
sleep_ms(2000)
busy_led.value(0)

DORMANT_PIN = 15

btn = Pin(DORMANT_PIN, Pin.IN, Pin.PULL_DOWN)
btn.irq(lambda e: print("button event!"),
        Pin.IRQ_RISING)

print("before lightsleep")
lowpower.lightsleep()
print("after lightsleep")

busy_led.value(1)
sleep_ms(2000)
busy_led.value(0)

print("before dormant")
lowpower.dormant_until_pin(DORMANT_PIN)
print("after dormant")

busy_led.value(1)
