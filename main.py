#!/usr/bin/python3

# **************************** Directory Structure ****************************
# FILE NAME SCHEME
# year-month-day_hour-minutes.jpg
#
# LOCAL PATHS
# ~/Time_Lapse/{year}/{FILE NAME}
#
# REMOTE PATHS
# This portion of the code only applies if you are backing up your images on
# a server. Also note, that in order to upload these files to your server, it
# uses FTP services. Checking to make sure the directory in question exists
# is not currently supported. So be sure to make the directories before hand.
# /home/{account}/RaspiZ/{pi's hostname}/{year}/{FILE NAME}

from csvlogger import CSVLogger
from twitter import Tweet
from backup import Backup
from report import Report
import core

logger = CSVLogger()
report = Report()


def main():
    # Acquires path and file related information
    path, file_name, local_path = core.file_info()

    # Captures the image for the day
    core.capture(local_path)

    # Adds the watermarks to the image just taken
    core.add_watermarks(path, file_name)

    # Transfers photo to your server
    backup = Backup()
    server, dropbox, gdrive = backup.file(local_path)

    # Tweet Daily Image
    successful_tweet = Tweet.post_image(local_path, logger.number_of_entries())

    # Logs the data from the photo captured into a CSV file
    logger.log_capture(file_name, local_path, server, dropbox, gdrive, successful_tweet)

    # Creates the daily report
    logger.file(report)

    # Email daily report and photo to the given email addresses
    core.email_report(file_name)


main()
