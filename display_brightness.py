#!/bin/python3

import screen_brightness_control as sbc

import argparse, yaml, geocoder, os

from suntime import Sun
from datetime import datetime, timezone, timedelta

def get_times():
    """
    get current time (ct), sunset (ss) time and sunrise (ss) time 
    for the current lattiude and longitude
    """
    
    latitude, longitude = geocoder.ip('me').latlng

    sun = Sun(latitude, longitude)

    current_time = datetime.now(timezone.utc)
    today_ss = sun.get_sunset_time()
    today_sr = sun.get_sunrise_time()

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
        description="Screen dimmer for your monitors",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
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
    parser.add_argument('--delta', '-d',
        help='Set delta for minutes before sunrise and after sunset for\
         the brightness to be adjusted',
        required=False,
        default=20
    )
    parser.add_argument('--toggle', '-tg',
        help='Toggle brightness level to and from "max" and "min"',
        required=False,
        action="store_true"
    )
    return parser.parse_args()

def load_config(location="config.yaml"):
    """Load the config"""
    with open(location, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except Exception as exc:

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
    if args.toggle:
        brightness = sbc.get_brightness()
        if brightness == list(config["brightness_values"]["max"].values()):
            level="min"
        elif brightness == list(config["brightness_values"]["min"].values()):
            level="max"
    elif args.level:
        level = args.level
    elif args.time:
        ct, sr, ss = get_times()

        if args.delta:
            sr += timedelta(minutes=int(args.delta))
            ss += timedelta(minutes=int(args.delta))

        if ct <= sr: # current time less than or equal sunrise time (no sun)
            level = "min"
        elif ct <= ss: # current time less than or equal to sunset time (sun)
            level = "max"
        else: # current time more than sunset time (no sun)
            level = "min"

    return level

def main():
    config_path = os.path.join(
        os.path.split(os.path.realpath(__file__))[0],
        "config.yaml"
    )
    config = load_config(config_path)
    args = parse_args(config)
    brightness_level = set_brightness_level(args, config)
    displays = config["brightness_values"][brightness_level].keys()
    set_brightness(config, displays, brightness_level)

if __name__ == "__main__":
    main()