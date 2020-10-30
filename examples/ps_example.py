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

from pyanalogdiscovery2 import PyAnalogDiscovery2, PyAnalogDiscovery2Exception, Configuration
import time

# This examples demonstrates how to use the Power Supply functionality
# It uses and V+ Power Supply line on a Analog Discovery 2.

try:
    # Power Supply Configuration
    voltage_level = 1.0
    current_limit = 0.5

    analogdiscovery2 = PyAnalogDiscovery2(Configuration.SCOPE_8K_WAVEGEN_4K_LOGIC_4K_PATTERNS_1K)
    ps = analogdiscovery2.acquire_power_supply()

    ps.configure_positive_voltage_supply_output(voltage_level, current_limit)
    ps.enable_all_outputs(True)

    for i in range(5):
        time.sleep(1)
        voltage_measurement, current_measurement = ps.read_positive_supply_output()
        print("Measurement [%d]: %f V\t%f A" % (i, voltage_measurement, current_measurement))

except PyAnalogDiscovery2Exception as e:
    print("Error/Warning %d occurred\n%s" % (e.status, e))
finally:
    analogdiscovery2.release()

# Console Output
# -----------------------
# Measurement [0]: 1.000000 V	1.000000 A
# Measurement [1]: 1.000000 V	1.000000 A
# Measurement [2]: 1.000000 V	1.000000 A
# Measurement [3]: 1.000000 V	1.000000 A
# Measurement [4]: 1.000000 V	1.000000 A
