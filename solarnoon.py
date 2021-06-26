from global_variables import GeneralSettings
from dateutil.parser import parse
from dateutil import tz
import requests


def get_time():
    lon = str(GeneralSettings.lon)
    lat = str(GeneralSettings.lat)
    result = requests.get("https://api.sunrise-sunset.org/json?lat={}&lng={}&date=today&formatted=0".format(lat, lon))
    data = result.json()
    time_str = data["results"]["solar_noon"]
    local_tz = tz.tzlocal()
    date_time = parse(time_str)
    local_time = date_time.astimezone(local_tz)

    return local_time.time()