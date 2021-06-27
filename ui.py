import os, pystray
import display_brightness as dpb

from pystray import Icon as icon, Menu as menu, MenuItem as item

from PIL import Image, ImageDraw

def load_image():
    """load icon"""
    image = Image.open(os.path.join(
        os.path.split(os.path.realpath(__file__))[0],
        "icon.png"
    ))
    return image

def quit_program(icon):
    """quit the systray icon"""
    icon.stop()

def dpb_do(icon, option):
    """perform dpb action based on the option string passed in"""
    args, config = dpb.init() # Maybe improve? Have to read every time

    if option.text == "Toggle":
        args.toggle = True
        dpb.set_brightness_level(args, config)

    elif option.text == "Config(min)":
        args.level = "min"
        dpb.set_brightness_level(args, config)

    elif option.text == "Config(max)":
        args.level = "max"
        dpb.set_brightness_level(args, config)
    elif option.text == "Default":
        args.level = "default"
        dpb.set_brightness_level(args, config)

    elif option.text == "Webcam": # how to exit?
        args.webcam = True
        dpb.set_brightness_level(args, config)
    elif option.text == "Time based": # how to exit?
        args.time = True
        dpb.set_brightness_level(args, config)

def main():
    icon('test', load_image(), 
        menu=menu(
            item(
                'Default',
                dpb_do
            ),
            item(
                'Config(min)',
                dpb_do
            ),
            item(
                'Config(max)',
                dpb_do
            ),
            item(
                'Webcam',
                dpb_do
            ),
            item(
                'Time based',
                dpb_do
            ),
            item(
                'Toggle',
                dpb_do
            ),
            item(
                'Quit',
                quit_program
            )
        )
    ).run()

if __name__ == "__main__":
    main()
    # https://pystray.readthedocs.io/en/latest/usage.html

