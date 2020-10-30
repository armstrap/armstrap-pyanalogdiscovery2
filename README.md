# Armstrap pyAnalogDiscovery2
Python wrappers to control Digilent Analog Discovery 2.  These wrappers call into the official c-driver, allowing you to control Analog Discover 2 from a Python application.

THIS IS NOT A COMPLETE API.  IT IS A WORK IN PROGRESS.

![AnalogDiscovery2](https://github.com/armstrap/armstrap-pyanalogdiscovery2/raw/master/images/digilent-analog-discovery-2.png)
![Python](https://github.com/armstrap/armstrap-pyanalogdiscovery2/raw/master/images/python-logo-and-wordmark.png)

# What is Digilent Analog Discovery 2?

Digilent Analog Discovery 2 is a USB oscilloscope, logic analyzer, and multi-function instrument that allows users to measure, visualize, generate, record, and control mixed-signal circuits of all kinds. Developed in conjunction with Analog Devices and supported by Xilinx University Program. This test and measurement device is small enough to fit in your pocket, but powerful enough to replace a stack of lab equipment, providing engineering professionals, students, hobbyists, and electronic enthusiasts the freedom to work with analog and digital circuits in virtually any environment, in or out of the lab. The analog and digital inputs and outputs can be connected to a circuit using simple wire probes; alternatively, the Analog Discovery BNC Adapter and BNC probes can be used to connect and utilize the inputs and outputs.

More information can be found on [digilent.com](https://store.digilentinc.com).

## Requirements
* [Digilent Analog Discover 2 hardware](https://store.digilentinc.com/analog-discovery-2-100msps-usb-oscilloscope-logic-analyzer-and-variable-power-supply/)
* [Latest Digilent Waveforms software](https://reference.digilentinc.com/reference/software/waveforms/waveforms-3/previous-versions)
* [Python >= 3.4](https://www.python.org/downloads/)

## Quickstart Guide

Run the following on a Command Line terminal

### Mac/Linux
```
git clone https://github.com/armstrap/armstrap-pyanalogdiscovery2.git
cd armstrap-pyanalogdiscovery2
export PYTHONPATH=lib
python examples/ps_example.py
```

### Windows
```
git clone https://github.com/armstrap/armstrap-pyanalogdiscovery2.git
cd armstrap-pyanalogdiscovery2
set PYTHONPATH=lib
python examples\ps_example.py
```
