from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from global_variables import EmailSettings
import smtplib

class Emailer:

    attachments = []

    def __init__(self, recipients, subject: str, body: str):
        self.recipients = recipients
        self.subject = subject
        self.body = body

    def send(self):
        msg = MIMEMultipart()
        msg["From"] = EmailSettings.email
        msg["To"] = ", ".join(self.recipients)
        msg["Subject"] = self.subject
        msg.attach(MIMEText(self.body, "plain"))

        for attachment in self.attachments:
            split = attachment.split("/")
            name = split[-1]
            file = MIMEApplication(open(attachment, "rb").read(),
                                   _subtype="txt")
            file.add_header("Content-Disposition", "attachment", filename=name)
            msg.attach(file)

        server = smtplib.SMTP(EmailSettings.server, EmailSettings.port)
        server.starttls()
        server.login(EmailSettings.email, EmailSettings.password)
        server.sendmail(EmailSettings.email, self.recipients, msg.as_string())

        server.quit()

    def attach(self, file: str):
        self.attachments.append(file)
