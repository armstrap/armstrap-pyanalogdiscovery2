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

from ctypes import create_string_buffer, c_double, c_uint8, c_int, cdll, byref
from enum import IntEnum
import sys

class Pins(IntEnum):
    DIO_0 = 0
    DIO_1 = 1
    DIO_2 = 2
    DIO_3 = 3
    DIO_4 = 4
    DIO_5 = 5
    DIO_6 = 6
    DIO_7 = 7
    DIO_8 = 8
    DIO_9 = 9
    DIO_10 = 10
    DIO_11 = 11
    DIO_12 = 12
    DIO_13 = 13
    DIO_14 = 14
    DIO_15 = 15
    def __str__(self):
        return self.name.replace("_", " ").title()

class AnalogIoChannel(IntEnum):
    POSITIVE_SUPPLY = 0
    NEGATIVE_SUPPLY = 1
    def __str__(self):
        return self.name.replace("_", " ").title()

class AnalogIoProperty(IntEnum):
    ENABLE = 0
    VOLTAGE = 1
    CURRENT = 2
    def __str__(self):
        return self.name.replace("_", " ").title()

class I2cClockRate(IntEnum):
    ONE_HUNDRED_KHZ = 100000
    FOUR_HUNDRED_KHZ = 400000
    ONE_MHZ = 1000000
    def __str__(self):
        return self.name.replace("_", " ").title()

class ClockPhase(IntEnum):
    FIRST_EDGE = 0
    SECOND_EDGE = 1
    def __str__(self):
        return self.name.replace("_", " ").title()

class Polarity(IntEnum):
    IDLE_LOW = 0
    IDLE_HIGH = 1
    def __str__(self):
        return self.name.replace("_", " ").title()

class Status(IntEnum):
    SUCCESS = 0
    ERROR_FAILED_TO_OPEN_DEVICE = -1
    ERROR_I2C_BUS_ERROR_CHECK_THE_PULLUPS = -2
    def __str__(self):
        return self.name.replace("_", " ").title()

class PyAnalogDiscovery2Exception(Exception):
    def __init__(self, status, dwf, hdwf):
        self.status = status
        self.dwf = dwf
        self.hdwf = hdwf

    def __str__(self):
        string_buffer = create_string_buffer(512)
        self.dwf.FDwfGetLastErrorMsg(string_buffer)
        if (len(string_buffer.value) == 0):
            return str(self.status)
        else:
            return str(self.status) + "\n" + str(string_buffer.value.decode('utf-8'))

class Configuration(IntEnum):
    SCOPE_8K_WAVEGEN_4K_LOGIC_4K_PATTERNS_1K = 0
    SCOPE_16K_WAVEGEN_1K_LOGIC_1K_PATTERNS_NONE = 1
    SCOPE_2K_WAVEGEN_16K_LOGIC_NONE_PATTERNS_NONE = 2
    SCOPE_512_WAVEGEN_256_LOGIC_16K_PATTERNS_16K = 3
    SCOPE_8K_WAVEGEN_4K_LOGIC_4K_PATTERNS_1K_1V8 = 4
    SCOPE_8K_WAVEGEN_4K_LOGIC_2K_PATTERNS_256_POWER = 5
    SCOPE_512_WAVEGEN_256_LOGIC_16K_PATTERNS_16K_1V8 = 6
    def __str__(self):
        return self.name.replace("_", " ").title()

class PyAnalogDiscovery2:
    '''Analog Discovery 2 is a hardware device sold by Digilent which
       integrates a mixed-signal oscilloscope, function generator, digital
       multimeter, programmable DC power supply, and digital I/O into a single
       form-factor device.  This class simply wraps that C-API, allowing us
       to control the device from python.
    '''
    def __init__(self, configuration, device_index = -1, device_name = ''):
        ''' Initialize the Analog Discovery 2 library.  This must be called at least
            once for the application.
        '''
        self.device_name = device_name
        if sys.platform.startswith("win"):
            self.dwf = cdll.LoadLibrary("dwf.dll")
        elif sys.platform.startswith("darwin"):
            self.dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
        else:
            self.dwf = cdll.LoadLibrary("libdwf.so")
        self.hdwf = c_int(0)
        self.dwf.FDwfDeviceConfigOpen(c_int(device_index), c_int(configuration), byref(self.hdwf))
        if (self.hdwf.value == 0):
            raise PyAnalogDiscovery2Exception(Status.ERROR_FAILED_TO_OPEN_DEVICE, self.dwf, self.hdwf)

    def release(self):
        ''' Finalize the AnalogDiscovery2 library.
        '''
        self.dwf.FDwfDeviceClose(self.hdwf)
        self.dwf = None
        self.hdwf = None

#------------------------------------------------------------------------------

    def acquire_power_supply(self):
        ''' Establishes communication with the power supply device. This method
            should be called once per session.
        '''
        return self.PowerSupply(self)

    class PowerSupply(object):
        def __init__(self, outer):
            self.dwf =  outer.dwf
            self.hdwf = outer.hdwf

        def configure_positive_voltage_supply_output(self, voltage_level, current_limit):
            ''' Configures a positive voltage output on the V+ pin. This
                method should be called once for every channel you want to
                configure to output voltage.
            '''
            if (voltage_level >= 0):
                self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, c_int(AnalogIoChannel.POSITIVE_SUPPLY), c_int(AnalogIoProperty.ENABLE), c_double(True))
                self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, c_int(AnalogIoChannel.POSITIVE_SUPPLY), c_int(AnalogIoProperty.VOLTAGE), c_double(voltage_level))
                self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, c_int(AnalogIoChannel.POSITIVE_SUPPLY), c_int(AnalogIoProperty.CURRENT), c_double(current_limit))

        def configure_negative_voltage_supply_output(self, voltage_level, current_limit):
            ''' Configures a voltage output on the specified channel. This
                method should be called once for every channel you want to
                configure to output voltage.
            '''
            if (voltage_level <= 0):
                self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, c_int(AnalogIoChannel.NEGATIVE_SUPPLY), c_int(AnalogIoProperty.ENABLE), c_double(True))
                self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, c_int(AnalogIoChannel.NEGATIVE_SUPPLY), c_int(AnalogIoProperty.VOLTAGE), c_double(voltage_level))
                self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, c_int(AnalogIoChannel.NEGATIVE_SUPPLY), c_int(AnalogIoProperty.CURRENT), c_double(current_limit))

        def enable_all_outputs(self, enable_outputs):
            ''' Enables or disables all outputs on all channels of the
                instrument.
            '''
            self.dwf.FDwfAnalogIOEnableSet(self.hdwf, c_int(enable_outputs))

        def read_positive_supply_output(self):
            ''' Reads the voltage and current levels of the specified channel.
            '''
            actual_voltage_level = c_double(0.0)
            actual_current_level = c_double(0.0)
            if (self.dwf.FDwfAnalogIOStatus(self.hdwf) != 0):
                self.dwf.FDwfAnalogIOChannelNodeStatus(self.hdwf, c_int(AnalogIoChannel.POSITIVE_SUPPLY), c_int(AnalogIoProperty.VOLTAGE), byref(actual_voltage_level))
                self.dwf.FDwfAnalogIOChannelNodeStatus(self.hdwf, c_int(AnalogIoChannel.POSITIVE_SUPPLY), c_int(AnalogIoProperty.CURRENT), byref(actual_current_level))
            return actual_voltage_level.value, actual_current_level.value

        def read_negative_supply_output(self):
            ''' Reads the voltage and current levels of the specified channel.
            '''
            actual_voltage_level = c_double(0.0)
            actual_current_level = c_double(0.0)
            if (self.dwf.FDwfAnalogIOStatus(self.hdwf) != 0):
                self.dwf.FDwfAnalogIOChannelNodeStatus(self.hdwf, c_int(AnalogIoChannel.POSITIVE_SUPPLY), c_int(AnalogIoProperty.VOLTAGE), byref(actual_voltage_level))
                self.dwf.FDwfAnalogIOChannelNodeStatus(self.hdwf, c_int(AnalogIoChannel.POSITIVE_SUPPLY), c_int(AnalogIoProperty.CURRENT), byref(actual_current_level))
            return actual_voltage_level.value, actual_current_level.value

#------------------------------------------------------------------------------

    def acquire_serial_peripheral_interface(self, reset = True):
        ''' Creates and returns a new SPI session for the device. The session 
            is used in all subsequent SPI method calls. This method should be
            called once per session.

            SPI bus mastering—You can use AnalogDiscovery2 digital I/O to
            interface to serial peripherals. When you configure a SPI bus, a set
            of lines are reserved for the bus and each line's direction is
            automatically configured.
        '''
        return self.SerialPeripheralInterface(self, reset)

    class SerialPeripheralInterface(object):
        def __init__(self, outer, reset):
            self.dwf =  outer.dwf
            self.hdwf = outer.hdwf

            # Some sensible default values
            self.clock_rate = 10000000.0 # 10MHz
            self.clock_polarity = Polarity.IDLE_LOW
            self.clock_phase = ClockPhase.FIRST_EDGE
            self.chip_select_polarity = Polarity.IDLE_HIGH
            self.cs = Pins.DIO_0
            self.sclk = Pins.DIO_1
            self.mosi = Pins.DIO_2
            self.miso = Pins.DIO_3

            if (reset == True):
                self.dwf.FDwfDigitalSpiReset()

        def configure_bus(self, cs, sclk, mosi, miso, clock_rate, clock_polarity = Polarity.IDLE_LOW, clock_phase = ClockPhase.FIRST_EDGE, chip_select_polarity = Polarity.IDLE_HIGH):
            ''' Configures the basic parameters of the SPI engine.
            '''
            self.cs = cs
            self.sclk = sclk
            self.mosi = mosi
            self.miso = miso
            self.clock_rate = clock_rate
            self.clock_polarity = clock_polarity
            self.clock_phase = clock_phase
            self.chip_select_polarity = chip_select_polarity

            self.dwf.FDwfDigitalSpiFrequencySet(self.hdwf, c_double(self.clock_rate))
            self.dwf.FDwfDigitalSpiClockSet(self.hdwf, c_int(self.sclk))

            self.dwf.FDwfDigitalSpiDataSet(self.hdwf, c_int(0), c_int(mosi)) # 0 DQ0_MOSI_SISO
            self.dwf.FDwfDigitalSpiDataSet(self.hdwf, c_int(1), c_int(miso)) # 1 DQ1_MISO

            spi_mode = 0
            if clock_polarity == Polarity.IDLE_LOW and clock_phase == ClockPhase.FIRST_EDGE:
                spi_mode = 0
            elif clock_polarity == Polarity.IDLE_LOW and clock_phase == ClockPhase.SECOND_EDGE:
                spi_mode = 1
            elif clock_polarity == Polarity.IDLE_HIGH and clock_phase == ClockPhase.FIRST_EDGE:
                spi_mode = 2
            elif clock_polarity == Polarity.IDLE_HIGH and clock_phase == ClockPhase.SECOND_EDGE:
                spi_mode = 3
            self.dwf.FDwfDigitalSpiModeSet(self.hdwf, c_int(spi_mode))
            self.dwf.FDwfDigitalSpiOrderSet(self.hdwf, c_int(1)) # 1 MSB first
            self.dwf.FDwfDigitalSpiSelect(self.hdwf, c_int(self.cs), c_int(chip_select_polarity))

        def write_read(self, write_data, read_data_size):
            ''' Completes a transaction on the bus by writing the provided data
                to MOSI and returning the data read on MISO.
            '''
            read_data_out = []
            read_data = (c_uint8 * read_data_size)()
            local_write_data = (c_uint8 * len(write_data))(*write_data)
            # Todo: FIX ME
            cdq = c_int(1)
            bits_per_word = c_int(8)
            
            # toggle Chip Select Line - ready to start communication
            if (self.chip_select_polarity == Polarity.IDLE_HIGH):
                self.dwf.FDwfDigitalSpiSelect(self.hdwf, c_int(self.cs), c_int(0)) # Pull low
            else:
                self.dwf.FDwfDigitalSpiSelect(self.hdwf, c_int(self.cs), c_int(1)) # Pull high

            self.dwf.FDwfDigitalSpiWriteRead(self.hdwf, cdq, bits_per_word, local_write_data, c_int(len(local_write_data)), byref(read_data), c_int(read_data_size))

            # toggle Chip Select Line - finished communication
            if (self.chip_select_polarity == Polarity.IDLE_HIGH):
                self.dwf.FDwfDigitalSpiSelect(self.hdwf, c_int(self.cs), c_int(1)) # Pull high (Idle)
            else:
                self.dwf.FDwfDigitalSpiSelect(self.hdwf, c_int(self.cs), c_int(0)) # Pull low

            for i in range(read_data_size): read_data_out.append(read_data[i])
            return read_data_out

        def reset_instrument(self):
            ''' Resets the session configuration to default values, and resets
                the device and driver software to a known state.
            '''
            self.dwf.FDwfDigitalSpiReset()


#------------------------------------------------------------------------------

    def acquire_inter_integrated_circuit(self, reset = True):
        ''' Creates and returns a new I2C session for the device. The session
            is used in all subsequent I2C method calls. This method should be
            called once per session.

            You can use AnalogDiscovery2 to master an I2C (Inter-Integrated Circuit)
            bus. When you configure an I2C bus, a set of lines are reserved for
            the bus and each line's direction is automatically configured.
        '''
        return self.InterIntegratedCircuit(self, reset)

    class InterIntegratedCircuit(object):
        def __init__(self, outer, reset):
            self.dwf =  outer.dwf
            self.hdwf = outer.hdwf
            self.address = 0
            if (reset == True):
                self.dwf.FDwfDigitalI2cReset()

        def configure_bus(self, i2c_clock_rate, address, scl_pin, sda_pin, clock_stretching_enabled = True):
            ''' Configures the basic parameters of the I2C engine.
            '''
            inak = c_int()
            self.address = address
            self.dwf.FDwfDigitalI2cRateSet(self.hdwf, c_double(i2c_clock_rate))
            self.dwf.FDwfDigitalI2cSclSet(self.hdwf, c_int(scl_pin))
            self.dwf.FDwfDigitalI2cSdaSet(self.hdwf, c_int(sda_pin))
            if (clock_stretching_enabled == True):
                self.dwf.FDwfDigitalI2cStretchSet(self.hdwf, c_int(1))
            else:
                self.dwf.FDwfDigitalI2cStretchSet(self.hdwf, c_int(0))
            self.dwf.FDwfDigitalI2cClear(self.hdwf, byref(inak))
            if (inak.value == 0):
                raise PyAnalogDiscovery2Exception(Status.ERROR_I2C_BUS_ERROR_CHECK_THE_PULLUPS, self.dwf, self.hdwf)

        def write_read(self, write_data, read_data_size):
            ''' Performs a write followed by read (combined format) on an I2C
                slave device.
            '''
            inak = c_int()
            read_data_out = []
            read_data = (c_uint8 * read_data_size)()
            write_data_len = c_int(len(write_data))
            local_write_data = (c_uint8 * write_data_len.value)(*write_data)
            self.dwf.FDwfDigitalI2cWriteRead(self.hdwf, c_int(self.address<<1), local_write_data, write_data_len, byref(read_data), c_int(read_data_size), byref(inak))
            if (inak.value != 0):
                print("Device Data NAK " + str(inak.value))
            for i in range(read_data_size): read_data_out.append(read_data[i])
            return read_data_out

        def reset_instrument(self):
            ''' Resets the session configuration to default values, and resets
                the device and driver software to a known state.
            '''
            self.dwf.FDwfDigitalI2cReset()

