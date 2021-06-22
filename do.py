#!/bin/python3

import screen_brightness_control as sbc
import argparse
import yaml

def parse_args():
    """parse passed in arguments"""
    parser = argparse.ArgumentParser(
        description="Screen dimmer for your monitors"
    )
    parser.add_argument('--max',
        help='Set brightness to max settings from config.yaml file',
        required=False, action="store_true"
    )
    parser.add_argument('--min',
        help='Set brightness to min settings from config.yaml file',
        required=False, action="store_true"
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
    """set the brightness for all the displays based on the config and the brightness level"""
    for display in displays:
        sbc.set_brightness(config[brightness_level][display], display=display)

def set_brightness_level(args, config):
    """set the brightness level based on the arguments or other parameters"""
    brightness_level = "min"
    if args.max:
        brightness_level = "max"
    return brightness_level

def main():
    args = parse_args()

    config = load_config("config.yaml")

    brightness_level = set_brightness_level(args, config)
    displays = config[brightness_level].keys()
    set_brightness(config, displays, brightness_level)

if __name__ == "__main__":
    main()