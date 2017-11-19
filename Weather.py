import math
import requests
from datetime import datetime
from random import randint
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageEnhance


class Weather:
    def __init__(self, resolution, picture):
        self.RESOLUTION = resolution
        self.picture = picture
        self.sunrise = None
        self.sunset = None
        self.current = None
        self.draw = ImageDraw.Draw(picture)
        self.sun_color = None
        self.sun_y = None
        self.key = self.get_api_key()
        self.zipcode = None
        self.season = self.get_season()
        self.load_assets()
    def get_api_key(self):
        """
        retrieves api key from api.txt and terminates otherwise.
        :return: key if api is found - None otherwise
        """
        with open("api.txt","r") as api_file:
            key = api_file.readline().strip()
            if key == "" or key == "{API HERE}":
                print("An API key is required to use this program.\n"
                      "Please create one at:\n "
                      "https://openweathermap.org/current")
            else:
                return key
        return None

    def get_location(self):
        print("Receiving location...")
        url = "https://ipinfo.io/json"

        response = requests.get(url)
        json = response.json()
        print(json)
        self.zipcode = json["postal"]
        lat_long = json["loc"].split(",")
        location = {"latitude": float(lat_long[0]),
                    "longitude": float(lat_long[1])
                    }
        print("You are in", location)
        return location

    def get_weather(self):
        """
        calls weather api using zipcode and retrieves
            weather as json
        :return: json of weather report
        """
        weather_request = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?zip=" + self.zipcode + ",us&appid=" + self.key)
        if weather_request.status_code != 200:
            print(weather_request.status_code)
            return
        json = weather_request.json()
        self.current = datetime.now().hour * 60 + datetime.now().minute
        sunrise_date = datetime.fromtimestamp(int(json["sys"]["sunrise"]))
        sunset_date = datetime.fromtimestamp(int(json["sys"]["sunset"]))
        self.sunrise = sunrise_date.hour * 60 + sunrise_date.minute
        self.sunset = sunset_date.hour * 60 + sunset_date.minute
        return json

    def draw_planet(self):
        """
        draws sun ellipse and colors sun based on day/night
        :return:
        """
        sunXY = self.get_sun_coordinates((self.sunrise < self.current and self.current < self.sunset))
        if self.current < self.sunrise or self.current > self.sunset:
            self.sun_color = (255, 255, 215)
        else:
            self.sun_color = (255, 255, 0)

        self.draw.ellipse((sunXY[0] - 48, sunXY[1] - 48, sunXY[0] + 48, sunXY[1] + 48), fill=self.sun_color)

    def get_sun_coordinates(self, isDay):
        """
        creates coordinates of sun based on screen Resolution
        :param isDay: Bool where Daytime = True
        :return: x,y coords of sun
        """
        if not isDay:
            current = self.current
            if self.current < self.sunrise:
                current = self.current + (24 * 60)
            elif self.current > self.sunset:
                current = self.current
            else:
                print("Error. Sun out during the night.\n{}\n{}\n{}".format(self.current, self.sunrise, self.sunset))
            sunrise = self.sunset
            sunset = (24 * 60) + self.sunrise
        else:
            current = self.current
            sunrise = self.sunrise
            sunset = self.sunset

        x = (current - sunrise) / (sunset - sunrise) * self.RESOLUTION[0]
        y = (self.RESOLUTION[1] / 2) - math.sin(((current - sunrise) /
                                                 (sunset - sunrise)) * (math.pi)) * (self.RESOLUTION[1] / 4)
        return (x, y)

    def get_sun_y(self):
        """
        Gets y coordinate of sun on the unit circle. -1: midnight && 1 : noon
        :return: normalized y coordinate of sun
        """
        offset = (3 * math.pi / 2)
        percent_through_Day = (self.current) / (24 * 60)

        self.sun_y = math.sin(2 * math.pi * percent_through_Day + offset)

    def set_sky_color(self):
        """
        Creates color of the sky based on light of sun and
            other multipliers.
        """
        sky_color_night = [11, 16, 85]
        sun_sky_color_multiplier = (self.sun_y + 1) / 2  # 0 -> .5 -> 1 -> .5 ...
        sky_color = (sky_color_night[0] + int(sun_sky_color_multiplier * 193),
                     sky_color_night[1] + int(sun_sky_color_multiplier * 239),
                     sky_color_night[2] + int(sun_sky_color_multiplier * 170))
        self.picture.paste(sky_color, [0, 0, self.RESOLUTION[0], self.RESOLUTION[1]])

    def write_text(self, temp, weather):
        """
        Writes text to the picture of temperature and weather.
        :param temp: temperature in Kalvin
        :param weather: description of weather: eg Cloudy
        """
        GRAY = (224, 224, 224)
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        day = weekdays[datetime.today().weekday()]
        date = "{} {}".format(str(datetime.today().day), months[datetime.today().month - 1])
        day_width, height = self.rockwell48.getsize(text=day)
        date_width = self.rockwell24.getsize(text=date)[0]
        temp_width = self.rockwell48.getsize(text=str(temp) + "°")[0]
        weather_width = self.rockwell24.getsize(text=str(weather))[0]
        left = max(temp_width + day_width, weather_width + date_width) + 48

        offset_x = 8
        offset_y = 16
        sep_x = 24
        sep_y = 8

        temp = int(float(((9 / 5) * (temp - 273) + 32)))
        self.draw.text((self.RESOLUTION[0] - left - offset_x, offset_y), day, font=self.rockwell48, fill=GRAY)
        self.draw.text((self.RESOLUTION[0] - left - offset_x + day_width + sep_x, offset_y),
                       str(temp) + "°", font=self.rockwell48, fill=GRAY)
        self.draw.text((self.RESOLUTION[0] - left - offset_x, offset_y + height + sep_y),
                       date, font=self.rockwell24, fill=GRAY)
        self.draw.text((self.RESOLUTION[0] - left - offset_x + date_width + sep_x,
                        offset_y + height + sep_y), str(weather), font=self.rockwell24, fill=GRAY)

    def draw_clouds(self, cloudiness):
        """
        draws clouds randomly -- 1 cloud per 10% cloudiness
        :param cloudiness: % cloudiness
        """
        sun_sky_color_multiplier = .25 + .75 * (1 + self.sun_y) / 2  # -1 -> 1 : .25 -> 1
        for i in range(len(self.cloud_lighting)):
            self.clouds[i] = self.cloud_lighting[i].enhance(sun_sky_color_multiplier)

        n = cloudiness // 10
        for i in range(n):
            x = (-200 + 500 * i % (self.RESOLUTION[0] - 200)) + randint(0, 500)
            y = randint(0, 400)
            position = (x, y)
            self.picture.paste(self.clouds[i % len(self.clouds)], position, self.clouds[i % len(self.clouds)])

    def get_season(self):
        """
        gets season based on current day.
        :return: season
        """
        day = datetime.now()
        season = ""
        if (day < datetime(datetime.now().year, 3, 21)) or (day > datetime(datetime.now().year, 12, 20)):
            season = "Winter"
        elif (day < datetime(datetime.now().year, 6, 21)):
            season = "Spring"
        elif (day < datetime(datetime.now().year, 9, 21)):
            season = "Summer"
        else:
            season = "Fall"
        return season

    def draw_ground(self):
        """
        draws ground based on season and lit with sun multiplier
        """
        sun_sky_color_multiplier = .25 + .75 * (1 + self.sun_y) / 2  # -1 -> 1 : .25 -> 1
        season_color = {
            "Winter": (255, 255, 255),
            "Spring": (153, 255, 153),
            "Summer": (51, 255, 51),
            "Fall": (51, 102, 0)
        }
        ground = Image.new("RGB", (self.RESOLUTION[0], 300), season_color[self.season])
        ground_lighting = ImageEnhance.Brightness(ground)
        ground = ground_lighting.enhance(sun_sky_color_multiplier)
        self.picture.paste(ground, (0, self.RESOLUTION[1] - 300))

    def update(self):
        """
        called to update entire picture.
        """
        print("Updating weather...")
        self.get_location()
        weather = self.get_weather()
        self.get_sun_y()
        self.set_sky_color()
        self.draw_planet()
        self.draw_clouds(weather["clouds"]["all"])
        self.draw_ground()

        self.write_text(weather["main"]["temp"], weather["weather"][0]["description"].title())

    def load_assets(self):
        """
        loads all of 'assets' folder
        :return:
        """
        self.rockwell48 = ImageFont.truetype(r"assets/ROCKB.ttf", 48)
        self.rockwell24 = ImageFont.truetype(r"assets/ROCKB.ttf", 24)
        self.clouds = [Image.open("assets/cloud{}.png".format(str(i))).convert("RGBA") for i in range(4)]
        self.cloud_lighting = [ImageEnhance.Brightness(i) for i in self.clouds]
