from datetime import datetime
from Sun import Sun
import requests



class LocationTime:
    def __init__(self):
        self.current_time = datetime.now().hour * 60 + datetime.now().minute
        self.lat_long = self.get_location()
        self.sunrise = None
        self.sunset = None
        self.get_sun_time()



    def get_location(self):
        print("Receiving location...")
        url = "https://ipinfo.io/json"

        response = requests.get(url)
        json = response.json()
        lat_long = json["loc"].split(",")
        location = {"latitude":float(lat_long[0]),
                    "longitude":float(lat_long[1])
                    }
        print("You are in",location)
        return location

    def get_sun_time(self):
        sun = Sun()
        eastern_offset = 60 * (-5)
        self.sunrise = sun.getSunriseTime(self.lat_long)["decimal"]*60 + eastern_offset
        self.sunset = sun.getSunsetTime(self.lat_long)["decimal"]*60 + eastern_offset


    def as_dictionary(self):

        return {
            "sunrise":self.sunrise,
            "sunset":self.sunset,
            "current":self.current_time
        }