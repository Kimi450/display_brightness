#!/bin/python3

import screen_brightness_control as sbc

import argparse, yaml, geocoder

from suntimes import SunTimes
from datetime import datetime, timezone


def get_times():
    """
    get current time (ct), sunset (ss) time and sunrise (ss) time 
    for the current lattiude and longitude
    """
    
    latitude, longitude = geocoder.ip('me').latlng

    sun = SunTimes(latitude, longitude)
    current_time = datetime.now(timezone.utc)
    today_sr = sun.riselocal(current_time)
    today_ss = sun.setlocal(current_time)

    return (current_time, today_sr, today_ss)

def format_times(times, time_format='%H:%M'):
    """format time in the given string time_format"""
    output = []
    if type(times) in (type([]), type(())):
        for time in times:
            output.append(format(time.strftime(time_format)))
    else:
        output = format(times.strftime(time_format))
    return output

def parse_args(config):
    """parse passed in arguments"""
    parser = argparse.ArgumentParser(
        description="Screen dimmer for your monitors"
    )
    parser.add_argument('--level', '-l',
        choices=list(config["brightness_values"].keys()),
        help='Set brightness level based on options from config.yaml file',
        required=False
    )
    parser.add_argument('--time', '-t',
        help='Set brightness level based on sunset and sunrise times',
        required=False,
        action="store_true"
    )
    return parser.parse_args()

def load_config(location="config.yaml"):
    """Load the config"""
    with open(location, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Error reading config file at: {location}")
            print(exc)
            exit(1)
    return config

def set_brightness(config, displays, brightness_level):
    """
    set the brightness for all the displays based on the config 
    and the brightness level
    """
    for display in displays:
        sbc.set_brightness(
            config["brightness_values"][brightness_level][display],
            display=display
        )
    return True

def set_brightness_level(args, config):
    """set the brightness level based on the argument(s) or other time"""
    level = "default"
    if args.level:
        level = args.level

    if args.time:    
        ct, sr, ss = get_times()
        if ct <= sr: # current time less than or equal sunrise time (no sun)
            level = "min"
        elif ct <= ss: # current time less than or equal to sunset time (sun)
            level = "max"
        else: # current time more than sunset time (no sun)
            level = "min"

    return level

def main():
    config = load_config("config.yaml")
    args = parse_args(config)
    brightness_level = set_brightness_level(args, config)
    displays = config["brightness_values"][brightness_level].keys()
    set_brightness(config, displays, brightness_level)

if __name__ == "__main__":
    main()