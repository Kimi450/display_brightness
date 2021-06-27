#!/bin/python3

import screen_brightness_control as sbc

import argparse, yaml, geocoder, os, math

from suntime import Sun
from datetime import datetime, timezone, timedelta

import cv2

import np
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
    parser.add_argument('--webcam', '-wc',
        help='Use your webcam to adjust brightness constantly',
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

    def cast_brightness_level_int(brightness_level):
        """
        cast brightness_level to an int and return, else return None
        """
        try:
            brightness_level = int(brightness_level)
            return brightness_level
        except Exception:
            return None

    if brightness_level_int := cast_brightness_level_int(brightness_level):
        # print(brightness_level_int)
        sbc.set_brightness(brightness_level_int)
    else:
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
        delta = 0
        if args.delta:
            delta = timedelta(minutes=int(args.delta))

        if ct <= sr - delta: # current time less than or equal sunrise time (no sun)
            level = "min"
        elif ct <= ss + delta: # current time less than or equal to sunset time (sun)
            level = "max"
        else: # current time more than sunset time (no sun)
            level = "min"

    return level

def get_frame_brightness(frame):
    """get frame brightness after converting to HSV format"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert it to hsv
    return hsv[...,2].mean()

def plateu_func(x, M=100, a=4/255):
    """platueing function for brightness, heuristic"""
    return 100*(1-math.e**(-a*x))

def linear_func(x):
    """linear function for brightness"""
    return frame_brightness*100/255

def read_webcam(config, displays):
    """
    constantly read the webcam and adjust brightness based on frame
    brightness. Press ESC to quit.
    """
    camera = cv2.VideoCapture(0)
    def read_frame(camera):
        """read the frame value and return adjusted brightness_level"""
        ret_val, frame = camera.read()
        frame_brightness = get_frame_brightness(frame)
        return plateu_func(frame_brightness)

    while True:
        brightness_level = read_frame(camera)
        set_brightness(config, displays, brightness_level)
        if cv2.waitKey(30) == 27: 
            break  # esc to quit
    return True

def main():
    config_path = os.path.join(
        os.path.split(os.path.realpath(__file__))[0],
        "config.yaml"
    )

    config = load_config(config_path)
    args = parse_args(config)

    sample_setting = list(config["brightness_values"].keys())[0]
    displays = config["brightness_values"][sample_setting].keys()

    brightness_level = set_brightness_level(args, config)

    if args.webcam:
        read_webcam(config, displays)
    else:
        set_brightness(config, displays, brightness_level)

if __name__ == "__main__":
    main()