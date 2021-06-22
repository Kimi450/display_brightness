#!/bin/python3

import screen_brightness_control as sbc

import argparse, yaml, geocoder

from suntime import Sun, SunTimeException
from datetime import datetime


def get_times():
    """get current time (ct), sunset (ss) time and sunrise (ss) time 
    for the current lattiude and longitude"""
    
    latitude, longitude = geocoder.ip('me').latlng

    sun = Sun(latitude, longitude)

    today_sr = sun.get_sunrise_time()
    today_ss = sun.get_sunset_time()
    current_time = datetime.now()

    return current_time, today_sr, today_ss

def format_time(time, time_format='%H:%M'):
    """format time in the given string time_format"""
    return format(time.strftime(time_format))

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
    """set the brightness for all the displays based on the config 
    and the brightness level
    """
    for display in displays:
        sbc.set_brightness(
            config["brightness_values"][brightness_level][display],
            display=display
        )
    return True

def set_brightness_level(args, config):
    """set the brightness level based on the argument(s) or other parameters"""
    return args.level

def main():
    config = load_config("config.yaml")
    args = parse_args(config)
    ct, sr, ss = get_times()
    print(get_times())
    brightness_level = set_brightness_level(args, config)
    displays = config["brightness_values"][brightness_level].keys()
    set_brightness(config, displays, brightness_level)

if __name__ == "__main__":
    main()