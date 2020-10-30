#! /usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2020 Charles Armstrap <charles@armstrap.org>
# If you like this library, consider donating to: http://bit.ly/pyanalogdiscovery2
# Anything helps.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pyanalogdiscovery2 import PyAnalogDiscovery2, PyAnalogDiscovery2Exception, Configuration, Polarity, ClockPhase, Pins

# This examples demonstrates how to master a SPI bus using the digital lines
# on a Digilent Analog Discovery 2.

try:
    # Hardware: ST iNEMO inertial module: always-on 3D accelerometer and 3D gyroscope
    # Company: STMicroelectronics
    # Part Number: LSM6DSO

    # For SPI wiring:
    # CS (Chip Select) output maps to Digital I/O Pin 0 on Analog Discovery 2 device
    # SCLK (Serial Clock) output maps to Digital I/O Pin 1 on Analog Discovery 2 device
    # MOSI (Master Out Slave In) input/output maps to Digital I/O Pin 2 on Analog Discovery 2 device
    # MISO (Master In Slave Out) input/output maps to Digital I/O Pin 3 on Analog Discovery 2 device
    cs = Pins.DIO_0
    sclk = Pins.DIO_1
    mosi = Pins.DIO_2
    miso = Pins.DIO_3

    # Channel Configuration
    clock_rate = 10000000.0 # 10MHz
    clock_polarity = Polarity.IDLE_LOW
    clock_phase = ClockPhase.FIRST_EDGE
    chip_select_polarity = Polarity.IDLE_HIGH

    # Data
    # Read operation (0x80) on WHO_AM_I register (0x0F) on attached SPI device
    # Read operation and register value are bitwise OR-ed together
    # According to the datasheet, we expect to read back the fixed CHIP_ID value of 0x6C
    data_to_write = [ 0x8F, 0 ]
    data_read_size = len(data_to_write)

    analogdiscovery2 = PyAnalogDiscovery2(Configuration.SCOPE_8K_WAVEGEN_4K_LOGIC_4K_PATTERNS_1K)
    spi = analogdiscovery2.acquire_serial_peripheral_interface()

    spi.configure_bus(cs, sclk, mosi, miso, clock_rate, clock_polarity, clock_phase, chip_select_polarity)

    # Write and read from the bus
    data_read = spi.write_read(data_to_write, data_read_size)

    print("Received %d bytes:" % len(data_read))
    for i in range(len(data_read)):
        print("[%d] = %d (0x%02x)" % (i, data_read[i], data_read[i]))

except PyAnalogDiscovery2Exception as e:
    print("Error/Warning %d occurred\n%s" % (e.status, e))
finally:
    analogdiscovery2.release()

# Console Output
# -----------------------
# Received 2 bytes:
# [0] = 0 (0x00)
# [1] = 108 (0x6c)
