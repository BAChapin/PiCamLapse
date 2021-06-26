from global_variables import GeneralSettings, WeatherSettings
from pyowm import OWM


def get_temp():
    owm = OWM(WeatherSettings.api_key)
    mgr = owm.weather_manager()
    one_call = mgr.one_call(lat=GeneralSettings.lat, lon=GeneralSettings.lon,
                            exclude="minutely,hourly",
                            units="imperial")

    return int(one_call.current.temperature().get("temp"))
