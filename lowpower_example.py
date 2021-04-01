from machine import Pin
from time import sleep

import lowpower

LED_BUSY = 25
busy_led = Pin(LED_BUSY, Pin.OUT)

DORMANT_PIN = 15

btn = Pin(DORMANT_PIN, Pin.IN, Pin.PULL_DOWN)
btn.irq(lambda e: print("button event!"),
        Pin.IRQ_RISING)

def blink_n_times(n):
    for _ in range(n):
        busy_led.value(1)
        sleep(0.5)
        busy_led.value(0)
        sleep(0.5)

while True:
    blink_n_times(1)
    print("before active loop")
    for _ in range(10**6):
        pass
    print("after active loop")

    blink_n_times(2)
    print("before sleep")
    sleep(10)
    print("after sleep")

    blink_n_times(3)
    print("before lightsleep")
    lowpower.lightsleep()
    print("after lightsleep")

    blink_n_times(4)
    print("before dormant")
    lowpower.dormant_until_pin(DORMANT_PIN)
    print("after dormant")
