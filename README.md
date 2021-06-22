# Project display_brightness

Change the brightness of all your monitors in one go. Currently, this project only works on Windows (tested on Windows 10). Run the commands in command promt or powershell.

## Setup of config.yaml

Every entry under the `brightness_values` section represents an option for your monitors' brightness levels. Check Usage for more information on how to switch to a setting.

Every entry under a setting represents the monitor and their respective brightness values [0-100]. Number 0 is reserved for the primary monitor. The rest mapped on a trial and error basis at the moment (change a value and see which monitor is changing brightness).

```yaml
brightness_values:
  default:
    0: 82
    1: 100
    2: 100
  max:
    0: 82
    1: 100
    2: 100
  
```

## Requirements

Install the following prerequisite python3 libraries
```bash
pip3 install screen_brightness_control pyyaml geocoder suntimes
```

## Usage

Get help

```bash
python3 display_brightness.py -h
```

Running the script without any arguments sets the brightness to `default`.

```bash
python3 display_brightness.py
```

Running the script with `-l` or `--level` allows you to set the level of brightness from the options defined in the `config.yaml` file.

```bash
python3 display_brightness.py -l max
```

Running the script with the `-t` or `--time` flag set enables automatic time based brightness control. 

Conditions are:

|              |    |              | Brightness level |
|--------------|----|--------------|------------------|
| Current Time | <= | Sunrise Time |       `min`      |
| Current Time | <= | Sunset Time  |       `max`      |
| Current Time | >  | Sunset time  |       `min`      |


allows you to set the level of brightness from the options defined in the `config.yaml` file.

```bash
python3 display_brightness.py -t
```