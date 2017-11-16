import math
from PIL import Image
from PIL import ImageDraw


class Weather:
    def __init__(self, resolution, picture, sun_dict):
        self.RESOLUTION = resolution
        self.picture = picture
        self.sun_dict = sun_dict
        self.sunrise = sun_dict["sunrise"]
        self.sunset = sun_dict["sunset"]
        self.current = sun_dict["current"]
        self.planet = ImageDraw.Draw(picture)
        self.sun_color = (255, 255, 0)

    def drawPlanet(self):
        sunXY = self.get_sun_coordinates((self.sunrise < self.current and self.current<self.sunset))
        self.planet.ellipse((sunXY[0] - 48, sunXY[1] - 48, sunXY[0] + 48, sunXY[1] + 48), fill=self.sun_color)

    def get_sun_coordinates(self, isDay):
        if not isDay:
            current = self.correct_current_time()
            sunrise = self.sunset
            sunset = (24*60) + self.sunrise
        else:
            current = self.current
            sunrise = self.sunrise
            sunset = self.sunset


        x = (current - sunrise) / (sunset - sunrise) * self.RESOLUTION[0]
        y = (self.RESOLUTION[1] / 2) - math.sin(((current - sunrise) /
                                                 (sunset - sunrise)) * (math.pi)) * (self.RESOLUTION[1] / 4)
        return (x, y)

    def correct_current_time(self):
        if self.current < self.sunrise:
            return self.current + (24 * 60)
        if self.current > self.sunset:
            return self.current
        print("Error. Sun out during the night.\n{}\n{}\n{}".format(self.current, self.sunrise, self.sunset))
        return self.current

    def set_sky_color(self):
        sky_color_night = [11, 16, 85]
        offset = (3 * math.pi / 2)
        percent_through_Day = (self.current) / (24 * 60)

        sun_y = math.sin(2 * math.pi * percent_through_Day + offset)
        sun_sky_color_multiplier = (sun_y + 1) / 2  # 0 -> .5 -> 1 -> .5 ...

        sky_color = (sky_color_night[0] + int(sun_sky_color_multiplier * 193),
                     sky_color_night[1] + int(sun_sky_color_multiplier * 239),
                     sky_color_night[2] + int(sun_sky_color_multiplier * 170))
        self.picture.paste(sky_color, [0, 0, self.RESOLUTION[0], self.RESOLUTION[1]])

    def update(self):
        print("Updating weather...")
        if self.current<self.sunrise or self.current>self.sunset:
            self.sun_color = (255,255,200)
        else:
            self.sun_color = (255,255,0)
        self.set_sky_color()
        self.drawPlanet()
