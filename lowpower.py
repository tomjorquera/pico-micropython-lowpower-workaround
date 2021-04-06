# Raspberry Pico micropython low-power workaround
# Copyright (C) 2021 Tom Jorquera
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

REG_IO_BANK0_BASE = 0x40014000
REG_IO_BANK0_INTR0 = 0x0f0
REG_IO_BANK0_DORMANT_WAKE_INTE0 = 0x160

IO_BANK0_DORMANT_WAKE_INTE0_GPIO0_EDGE_HIGH_BITS = 0x00000008
IO_BANK0_DORMANT_WAKE_INTE0_GPIO0_EDGE_LOW_BITS = 0x00000004
IO_BANK0_DORMANT_WAKE_INTE0_GPIO0_LEVEL_HIGH_BITS = 0x00000002
IO_BANK0_DORMANT_WAKE_INTE0_GPIO0_LEVEL_LOW_BITS = 0x00000001

REG_XOSC_BASE = 0x40024000
REG_XOSC_DORMANT = 0x08
REG_XOSC_STATUS = 0x04

XOSC_DORMANT_VALUE_DORMANT = 0x636f6d61
XOSC_STATUS_STABLE_BITS = 0x80000000

@micropython.asm_thumb
def _read_bits(r0):
    ldr(r0, [r0, 0])

@micropython.asm_thumb
def _write_bits(r0, r1):
    str(r1, [r0, 0])

def gpio_acknowledge_irq(gpio, events):
    _write_bits(REG_IO_BANK0_BASE + REG_IO_BANK0_INTR0 + int(gpio / 8) * 4,
                events << 4 * (gpio % 8))

def dormant_until_pins(gpio_pins, edge=True, high=True):
    low = not high
    level = not edge

    if level and low:
        event = IO_BANK0_DORMANT_WAKE_INTE0_GPIO0_LEVEL_LOW_BITS
    if level and high:
        event = IO_BANK0_DORMANT_WAKE_INTE0_GPIO0_LEVEL_HIGH_BITS
    if edge and low:
        event = IO_BANK0_DORMANT_WAKE_INTE0_GPIO0_EDGE_LOW_BITS
    if edge and high:
        event = IO_BANK0_DORMANT_WAKE_INTE0_GPIO0_EDGE_HIGH_BITS

    events = 0
    for gpio_pin in gpio_pins:
        gpio_acknowledge_irq(gpio_pin, event)

        # Enable Wake-up from GPIO IRQ
        gpio_acknowledge_irq(gpio_pin, event)
        en_reg = REG_IO_BANK0_BASE + REG_IO_BANK0_DORMANT_WAKE_INTE0 + int(gpio_pin / 8) * 4
        events += event << 4 * (gpio_pin % 8)
    _write_bits(en_reg, events)

    # Go dormant
    _write_bits(REG_XOSC_BASE + REG_XOSC_DORMANT,
                XOSC_DORMANT_VALUE_DORMANT)

    while not _read_bits(REG_XOSC_BASE + REG_XOSC_STATUS) & XOSC_STATUS_STABLE_BITS:
        pass

    for gpio_pin in gpio_pins:
        gpio_acknowledge_irq(gpio_pin, event)

def dormant_until_pin(gpio_pin, edge=True, high=True):
    dormant_until_pins([gpio_pin], edge, high)

@micropython.asm_thumb
def lightsleep():
    wfi()
