import os
import random
from .smtp_email import SmtpMail
from dotenv import load_dotenv
import redis
load_dotenv()

class EmailUtils:
    def __init__(self):
        self.mail=SmtpMail()
        self.app_name=os.getenv("APP_NAME")
        self.otp_len=int(os.getenv("OTP_LENGTH"))
        self.logo_url=os.getenv("APP_LOGO_URL", "")
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            db=int(os.getenv("REDIS_DB")),
            decode_responses=True
        )

    def generate_otp(self,email):
        otp = ''.join([str(random.randint(0, 9)) for _ in range(self.otp_len)])
        subject = f"{self.app_name} - Your OTP Code"
        html_content = f"""
                <html>
                    <body style="font-family: Arial, sans-serif;">
                        <div style="text-align:center;">
                            <img src="{self.logo_url}" alt="Logo" style="width:120px; margin-bottom:20px;" />
                            <h2>{self.app_name} - OTP Verification</h2>
                            <p>Your OTP code is:</p>
                            <div style="font-size:2em; font-weight:bold; margin:20px 0;">{otp}</div>
                            <p>This code is valid for a limited time. Please do not share it with anyone.</p>
                        </div>
                    </body>
                </html>
                """
        self.redis_client.setex(f"otp:{email}", 60, otp)
        return self.mail.send_mail(to=email,content=html_content,content_type="html",subject=subject)

    def validate_otp(self,otp,email):
        key = f"otp:{email}"
        stored_otp = self.redis_client.get(key)
        if stored_otp and stored_otp == otp:
            self.redis_client.delete(key)  # Invalidate OTP after successful validation
            return True
        return False
