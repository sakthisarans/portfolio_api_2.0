import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

class SmtpMail:
    def __init__(self):
        self.server = os.getenv("SMTP_SERVER")
        self.port = int(os.getenv("SMTP_PORT"))
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")

    def send_mail(self, to, subject, content, content_type):
        try:
            server = smtplib.SMTP(self.server, self.port)
            server.starttls()
            server.login(self.username, self.password)

            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.username
            message["To"] = to

            if content_type == 'text':
                mime_content = MIMEText(content, "plain")
            elif content_type == 'html':
                mime_content = MIMEText(content, "html")
            else:
                mime_content = MIMEText(content, "plain")

            message.attach(mime_content)

            server.sendmail(self.username, to, message.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False