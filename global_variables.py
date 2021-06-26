import json


class File:
    location = "/home/pi/PiCamLapse/config.json"
    _read = open(location, "r")
    data = json.load(_read)


class GeneralSettings:
    pi_identifier = File.data["pi_identifier"]
    base_path = File.data["base_path"]
    lat = File.data["latitude"]
    lon = File.data["longitude"]
    font_size = File.data["font_size"]
    font_path = File.data["font_path"]
    overwrite_image = File.data["overwrite"]


class ServerSettings:
    _data = File.data["sftp_settings"]
    enabled = _data["enabled"]
    host_address = _data["host_address"]
    username = _data["username"]
    password = _data["password"]


class DropboxSettings:
    _data = File.data["dropbox"]
    enabled = _data["enabled"]
    access_token = _data["access_token"]


class GDriveSettings:
    _data = File.data["google_drive"]
    enabled = _data["enabled"]
    parent_id = _data["parent_id"]
    year_id = _data["current_path"]["year_id"]
    year = _data["current_path"]["year"]
    
    def update_parent(id: str):
        with open(File.location, "w") as file:
            local_data = File.data
            local_data["google_drive"]["parent_id"] = id
            json.dump(local_data, file, indent=4)
        GDriveSettings.parent_id = id

    def update_year(id: str, year: int):
        with open(File.location, "w") as file:
            local_data = File.data
            local_data["google_drive"]["current_path"]["year_id"] = id
            local_data["google_drive"]["current_path"]["year"] = year
            json.dump(local_data, file, indent=4)
        GDriveSettings.year_id = id
        GDriveSettings.year = year


class WeatherSettings:
    _data = File.data["owm"]
    api_key = _data["api_key"]


class TwitterSettings:
    _data = File.data["twitter"]
    enabled = _data["enabled"]
    api_key = _data["api_key"]
    api_secret = _data["api_secret"]
    access_token = _data["access_token"]
    access_token_secret = _data["access_token_secret"]


class EmailSettings:
    _data = File.data["report_email"]
    server = _data["server"]
    port = _data["port"]
    email = _data["email"]
    password = _data["password"]
    recipients = _data["recipients"]
