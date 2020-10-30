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

from pyanalogdiscovery2 import PyAnalogDiscovery2, PyAnalogDiscovery2Exception, Configuration, I2cClockRate, Pins

# This examples demonstrates how to master an I2C bus using the digital lines
# on a Digilent Analog Discovery 2.

try:
    # Hardware: BOSCH Digital, triaxial acceleration sensor
    # Company: Bosch Sensortec 
    # Part Number: BMA456

    # For I2C wiring:
    # SCL (Serial Clock) output maps to Digital I/O Pin 0 on AnalogDiscovery2 device
    # SDA (Serial Data) input/output maps to Digital I/O Pin 1 on AnalogDiscovery2 device

    # For this to work, you need to pullup the SCL and SDA lines to VCC by manually
    # adding a 10K resistor from SCL to VCC and adding another 10K resistor from SDA to
    # VCC.
    scl = Pins.DIO_0
    sda = Pins.DIO_1

    # Channel Configuration
    clock_rate = I2cClockRate.ONE_HUNDRED_KHZ # 100kHz

    # You can find the i2c address by looking at the datasheet for your attached chip.
    # According to the datasheet, you also need to make sure you wire SDO line to GND
    # to signal the chip to use i2c address 0x18
    address = 0x18

    # Data
    # Read operation on CHIP_ID register (0x0) on attached I2C BMA456 device
    # According to the datasheet, we expect to read back the fixed CHIP_ID value of 0x16
    data_to_write = [ 0x0 ]
    data_read_size = len(data_to_write)

    analogdiscovery2 = PyAnalogDiscovery2(Configuration.SCOPE_8K_WAVEGEN_4K_LOGIC_4K_PATTERNS_1K)
    i2c = analogdiscovery2.acquire_inter_integrated_circuit()

    i2c.configure_bus(clock_rate, address, scl, sda)

    # Write and read from the bus
    data_read = i2c.write_read(data_to_write, data_read_size)

    print("Received %d bytes:" % len(data_read))
    for i in range(len(data_read)):
        print("[%d] = %d (0x%02x)" % (i, data_read[i], data_read[i]))

except PyAnalogDiscovery2Exception as e:
    print("Error/Warning %d occurred\n%s" % (e.status, e))
finally:
    analogdiscovery2.release()

# Console Output
# -----------------------
# Received 1 bytes:
# [0] = 22 (0x16)
