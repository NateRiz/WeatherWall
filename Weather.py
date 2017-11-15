import math
from PIL import ImageDraw
class Weather:
    def __init__(self,resolution, picture, sun_dict):
        self.RESOLUTION = resolution
        self.sun_dict = sun_dict
        self.sky_color = (204, 255, 255)
        self.sunrise = sun_dict["sunrise"]
        self.sunset = sun_dict["sunset"]
        self.current = sun_dict["current"]
        self.planet = ImageDraw.Draw(picture)

    def drawPlanet(self):
        sunXY = self.get_sun_coordinates()
        self.planet.ellipse((sunXY[0] - 32, sunXY[1] - 32, sunXY[0] + 32, sunXY[1] + 32), fill=(255, 255, 0, 255))

    def get_sun_coordinates(self):
        x = (self.current - self.sunrise) / (self.sunset - self.sunrise) * self.RESOLUTION[0]
        y = (self.RESOLUTION[1] / 2) - math.sin(((self.current - self.sunrise) /
                                                 (self.sunset - self.sunrise)) * (math.pi)) * (self.RESOLUTION[1] / 4)
        return (x, y)