from datetime import datetime
from report import Report
from weather import get_temp
import os
import csv

class CSVLogger:

    log_path = "photo_log.csv"
    field_names = ["Photo Number",
                   "Date",
                   "Temperature",
                   "Photo Title",
                   "Local Path",
                   "Twitter Post",
                   "Remote Path",
                   "Dropbox Path",
                   "GoogleDrive Path"]

    def number_of_entries(self):
        did_exist = os.path.exists(self.log_path)
        if did_exist:
            with open(self.log_path, "r") as file:
                reader = csv.DictReader(file, fieldnames=self.field_names)
                rows = list(reader)
                length = len(rows)
                if length <= 1:
                    return 0
                else:
                    return length - 1
        else:
            return 1

    def first_recorded_date(self):
        file = open(self.log_path)
        reader = csv.DictReader(file, fieldnames=self.field_names)
        rows = list(reader)
        if len(rows) > 1:
            first_date_entry = rows[1][self.field_names[1]]
            first_date = [int(x) for x in first_date_entry.split("-")]
            return datetime(first_date[0], first_date[1], first_date[2])
        else:
            return datetime.now()

    def last_record(self):
        file = open(self.log_path)
        reader = csv.DictReader(file, fieldnames=self.field_names)
        rows = list(reader)
        return rows[-1]

    def number_for_new_entry(self):
        first_date = self.first_recorded_date()
        days_since = (datetime.now() - first_date).days
        return days_since + 1

    def ready_for_video(self):
        return self.number_of_entries() % 365 == 0 and self.number_of_entries() is not 0

    def log_capture(self, file_name: str, local_path: str, remote_path: str, dropbox: str, gdrive: str, tweet: bool):
        did_exist = os.path.exists(self.log_path)
        with open(self.log_path, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.field_names)
            if not did_exist:
                writer.writeheader()

            date = datetime.now().strftime("%Y-%m-%d")
            dict = {self.field_names[0]: self.number_for_new_entry(),
                    self.field_names[1]: date,
                    self.field_names[2]: "{}°F".format(get_temp()),
                    self.field_names[3]: file_name,
                    self.field_names[4]: local_path,
                    self.field_names[5]: tweet,
                    self.field_names[6]: remote_path,
                    self.field_names[7]: dropbox,
                    self.field_names[8]: gdrive}

            writer.writerow(dict)

    def file(self, report: Report):
        report.section_header("Today's Report")
        report.write("Today's date is {}.".format(datetime.now()
                                                  .strftime("%Y-%m-%d")))

        first_date = self.first_recorded_date()
        days_since = (datetime.now() - first_date).days
        if days_since == 0:
            number_of_days = "today."
        elif days_since == 1:
            number_of_days = "yesterday."
        else:
            number_of_days = "{} days ago.".format(days_since)

        report.write("This project started on {0}, {1}"
                        .format(first_date.strftime("%Y-%m-%d"),
                                number_of_days))

        number_recorded = self.number_of_entries()
        next_line = "We've properly recorded {0} out of a possible {1}" \
                    " photos.".format(number_recorded, days_since + 1)
        report.write(next_line)

        self.report_last_entry(report)

        if number_recorded < days_since:
            self.error_report(report, number_recorded, days_since)

        report.close()

    def report_last_entry(self, report: Report):
        report.empty_line(2)
        report.section_header("Last Record")

        last_record = self.last_record()
        for field in self.field_names:
            field_length = len(field)
            needed_spaces = 20 - field_length
            if last_record[field] == "":
                report.write("{0}:{1}{2}".format(field, " " * needed_spaces,
                                                 "N/A"))
            else:
                report.write("{0}:{1}{2}".format(field, " " * needed_spaces,
                                                 last_record[field]))

    def error_report(self, report: Report, number_recorded: int, days_since : int):
        report.empty_line(2)
        number_missing = days_since - number_recorded
        report.section_alert("MISSING RECORDS")
        message = ("Since this program has been started, {0} photos have "
                   "not been taken. Whether this is due to a power outage "
                   "or some other technical malfunction is unknown."
                   .format(number_missing))

        report.write(message)
        report.empty_line()

        report.write("You're missing these photos on these dates:")
        self.missing_dates(report, number_missing)

    def missing_dates(self, report: Report, missing_records: int):
        missing_dates = 0
        file = open(self.log_path)
        reader = csv.DictReader(file, fieldnames=self.field_names)
        rows = list(reader)
        first_date = self.first_recorded_date()
        days_since = (datetime.now() - first_date).days

        for num in range(1, len(rows) + 1):
            photo_num = int(rows[num][self.field_names[0]])
            if photo_num is not num:
                days_ago = days_since - (num - 1)
                missing_date = datetime.now() - datetime.timedelta(days=days_ago)
                report.write("   {0} - {1}"
                             .format(num, missing_date.strftime("%Y-%m-%d")))
                missing_date += 1

            if missing_dates is missing_records:
                break
