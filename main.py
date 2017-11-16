from Weather import Weather
from PIL import Image
import time

RESOLUTION = (1920, 1080)
def main():

    picture = Image.new("RGB",RESOLUTION, 0)
    weather = Weather(RESOLUTION, picture)
    weather.update()

    picture.save("picture.png")





















if __name__ == '__main__':
    main()