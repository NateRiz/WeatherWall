import math
from PIL import ImageDraw
class Weather:
    def __init__(self,resolution, picture, sun_dict):
        self.RESOLUTION = resolution
        self.sun_dict = sun_dict
        self.sunrise = sun_dict["sunrise"]
        self.sunset = sun_dict["sunset"]
        self.current = sun_dict["current"]
        self.planet = ImageDraw.Draw(picture)
        self.sun_color = (255, 255, 0) # --> (0, 0, 51)
        self.sky_color = self.get_sky_color()


    def drawPlanet(self):
        sunXY = self.get_sun_coordinates(self.sunrise<self.current<self.sunset)
        self.planet.ellipse((sunXY[0] - 48, sunXY[1] - 48, sunXY[0] + 48, sunXY[1] + 48), fill=self.sun_color)

    def get_sun_coordinates(self, isDay = True):
        current = {True:self.current, False: self.correct_current_time()}[isDay]
        sunrise = {True:self.sunrise, False: self.sunset}[isDay]
        sunset = {True:self.sunset, False: (24*60)+self.sunrise}[isDay]

        print(sunrise, current, sunset)

        x = (current - sunrise) / (sunset - sunrise) * self.RESOLUTION[0]
        y = (self.RESOLUTION[1] / 2) - math.sin(((current - sunrise) /
                                                 (sunset - sunrise)) * (math.pi)) * (self.RESOLUTION[1] / 4)
        return (x, y)

    def correct_current_time(self):
        if self.current<self.sunrise:
            return self.current+(24*60)
        if self.current>self.sunset:
            return self.current
        print("Error. Sun out during the night.")
        return self.current

    def get_sky_color(self):
        pass