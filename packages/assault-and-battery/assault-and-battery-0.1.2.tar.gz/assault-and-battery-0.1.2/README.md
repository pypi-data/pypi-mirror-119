# Battery discharge calculator

This is a simple script that will calculate the discharge curve of a battery. It does
this by communicating with a flight controller running INAV (with calibrated voltage and
current sensors) with a constant load attached.

It reads the voltage, instant amperage, and Ah consumed, and writes the samples to a CSV
file for later plotting.


## Installation

Use pipx:

```bash
$ pipx install assault_and_battery
```

And run the script as:

```bash
$ assault --help
```

## Usage

Plug an FC with calibrated sensors to USB, making sure to either cut the VCC cable (or
put some tape over the VCC pin), or use Bluetooth, USB-Serial, or some other way that
doesn't power the FC. Also make sure to not have any ground loops.

Then, run the script and start your load. It will output a CSV file with the current
date and all the measurements.

To plot stuff, use `assault plot <csv file>`. You can delete the first few values if the
load hasn't ramped up, or if you want to get rid of starting noise. This will produce
a graph, that's about it.
