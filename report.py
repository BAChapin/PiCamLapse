# This object is for creating a daily report, indicating the progress of the
# currently running Time Lapse. The file structure is plain text with some
# slight formatting.
# Every section/seperator will be represented by '-' characters on both sides
# of the given text.
# Every alert will be represented similarly to that of a section header, but
# replacing the '-' for '*' characters. On each side of the chain of '*'
# characters will be '!'

class Report:

    fileName = "daily_report.txt"
    file = open(fileName, "w")
    line_length = 80

    def section_header(self, header: str):
        length = len(header) + 2
        number_of_indicators = (self.line_length - length) // 2
        separator = ("-" * number_of_indicators)
        line = "{0} {1} {0}".format(separator, header)
        self.file.write(line + "\n\n")

    def section_alert(self, alert: str):
        length = len(alert) + 6
        number_of_indicators = (self.line_length - length) // 2
        separator = ("*" * number_of_indicators)
        line = "!{0}! {1} !{0}!".format(separator, alert)
        self.file.write(line + "\n\n")

    def empty_line(self, count: int = 1):
        self.file.write("\n" * count)

    # This will write whatever text you pass into it, and it will automatically
    # wrap the text based upon the line_length specified.
    def write(self, content: str):
        if len(content) > self.line_length:
            content_words = content.split(" ")
            content_arr = []
            temp_line = ""

            for word in content_words:
                if len(temp_line) + (len(word) + 1) > self.line_length:
                    content_arr.append(temp_line + "\n")
                    temp_line = "{} ".format(word)
                else:
                    temp_line += "{} ".format(word)
            else:
                if len(temp_line) > 0:
                    content_arr.append(temp_line)
                self.file.writelines(content_arr)

        else:
            self.file.write(content + "\n")

    def close(self):
        self.file.close()
