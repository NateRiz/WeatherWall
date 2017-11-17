from Weather import Weather
from PIL import Image
import ctypes
import os
import time
RESOLUTION = (1920, 1080)

def main():
    picture = Image.new("RGB",RESOLUTION, 0)
    weather = Weather(RESOLUTION, picture)
    while 1:
        weather.update()
        picture.save("picture.png")
        make_wallpaper()
        time.sleep(3600) #30 minutes


def make_wallpaper():
    print("Creating wallpaper..")
    path = os.path.abspath(r"picture.png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)




















if __name__ == '__main__':
    main()