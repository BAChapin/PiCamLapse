from global_variables import GeneralSettings, EmailSettings
from imageproc import ImageProcessor, Position
from gpsconverter import GPSConverter
from emailer import Emailer
from datetime import datetime
from time import sleep
from picamera import PiCamera
import weather
import piexif


def file_info():
    now = datetime.now()
    year_path = now.strftime("%Y")
    formatted_date = now.strftime("%Y-%m-%d_%H-%M")
    file_name = "{}.jpg".format(formatted_date)
    path = "{0}/Time_Lapse/{1}/".format(GeneralSettings.base_path, year_path)
    local_path = path + file_name

    return path, file_name, local_path


def capture(path: str):
    converter = GPSConverter(GeneralSettings.lat, GeneralSettings.lon)
    with PiCamera() as camera:
        camera.resolution = (3280, 2464)
        camera.exif_tags["GPS.GPSLatitudeRef"] = converter.lat_ref()
        camera.exif_tags["GPS.GPSLatitude"] = converter.strlat()
        camera.exif_tags["GPS.GPSLongitudeRef"] = converter.lon_ref()
        camera.exif_tags["GPS.GPSLongitude"] = converter.strlon()
        camera.start_preview()
        sleep(0.1)
        camera.capture(path)


def data_from_photo(path: str):
    exif = piexif.load(path)
    image_date = str(exif["Exif"][piexif.ExifIFD.DateTimeOriginal])
    date_split = image_date.split(" ")
    image_day = date_split[0].split(":")
    image_time = date_split[1].split(":")
    watermark = "{0}-{1}-{2} {3}:{4}:{5}".format(image_day[0],
                                                 image_day[1],
                                                 image_day[2],
                                                 image_time[0],
                                                 image_time[1],
                                                 image_time[2])

    return watermark.translate({ord(i): None for i in "b'"}), piexif.dump(exif)


def add_watermarks(dir: str, file_name: str):
    date_watermark, data = data_from_photo(dir + file_name)
    processor = ImageProcessor(dir, file_name, GeneralSettings.overwrite_image)
    new_path = processor.place_at(date_watermark, Position.BottomRight, 50)

    weather_watermark = "Temperature: {}°F".format(weather.get_temp())
    new_path = processor.place_at(weather_watermark, Position.BottomLeft, 50)

    piexif.insert(data, new_path)


def email_report(file_name):
    date = datetime.now()
    year = date.strftime("%Y")

    log_file_path = "photo_log.csv"
    report_file_path = "daily_report.txt"
    photo_file_path = "{}/Time_Lapse/{}/{}".format(GeneralSettings.base_path, year, file_name)

    subject = "Daily report from: {}".format(GeneralSettings.pi_identifier)
    
    with open(report_file_path, "r") as file:
        daily_report = file.read()

        email_service = Emailer(EmailSettings.recipients, subject, daily_report)
        email_service.attach(log_file_path)
        email_service.attach(photo_file_path)

        email_service.send()