from Weather import Weather
from PIL import Image
from LocationTime import LocationTime
import time

RESOLUTION = (1920, 1080)
def main():

    picture = Image.new("RGB",RESOLUTION, 0)
    loc_time = LocationTime()
    sun_dict = loc_time.as_dictionary()
    print("Current Time : {}\nSunrise : {}\nSunset : {}".format(sun_dict["current"], sun_dict["sunrise"], sun_dict["sunset"]))
    weather = Weather(RESOLUTION, picture, sun_dict)
    weather.drawPlanet()
    picture.save("picture.png")






















if __name__ == '__main__':
    main()