# Project display_brightness

Change the brightness of all your monitors in one go. Currently, this project only works on Windows (tested on Windows 10). Run the commands in command promt or powershell.

## AutoHotKey (AHK)

Also provided is an AHK script which can be used to setup shortcuts. 

Defaults are:
| Key combination | Action                           |
|-----------------|----------------------------------|
|Windows Key + `  | display_brightness.py -tg        |
|Windows Key + 1  | display_brightness.py -l max     |
|Windows Key + 2  | display_brightness.py -l 50      |
|Windows Key + 3  | display_brightness.py -l min     |
|Windows Key + 4  | display_brightness.py -l custom  |
|Windows Key + 5  | display_brightness.py -wc        |

1. Download and install [AutoHotKey](https://www.autohotkey.com/)
2. Make sure you change the location of the `display_brightness.py` script in the AHK file. 
3. Run the .ahk file and check it works correctly
4. Make Windows/your OS run it on startup, check [here for Windows 10/11](https://www.thewindowsclub.com/how-to-run-cmd-command-on-startup-automatically-in-windows)

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
pip3 install screen_brightness_control pyyaml geocoder suntime opencv-python
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

Running the script with `-tg` or `-toggle` will toggle the brightness between `min` and `max` settings.

```bash
python3 display_brightness.py -tg
```

Running the script with `-l` or `--level` allows you to set the level of brightness from the options defined in the `config.yaml` file. A number [0-100] can be used as well to set the brightness for all monitors.

```bash
python3 display_brightness.py -l max
```

Running the script with `-wc` or `--webcam` uses your webcam to detect the brightness levels in the room and adjust the brightness level accordingly.

```bash
python3 display_brightness.py -wc
```

Running the script with the `-t` or `--time` flag set enables automatic time based brightness control. 
Adding `-d DELTA` or `--delta DELTA` to it will allow you to set a custom delta in minutes, default value is 20 minutes. 

Conditions are:

|              |    |                      | Brightness level |
|--------------|----|----------------------|------------------|
| Current Time | <= | Sunrise Time - DELTA |       `min`      |
| Current Time | <= | Sunset Time  + DELTA |       `max`      |
| Current Time | >  | Sunset time  + DELTA |       `min`      |

```bash
python3 display_brightness.py -t [-d 20]
```

Start the UI by running the following command, and select the options from the system tray icon. 

```bash
python3 ui.py
```
