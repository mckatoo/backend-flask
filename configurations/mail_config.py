import smtplib
from configurations.envs_config import (
    SMTP_SERVER_ADDRESS,
    SMTP_SERVER_PORT,
    SMTP_PASSWORD,
    SMTP_START_TLS,
    SMTP_USERNAME,
)

from email.message import EmailMessage


def send_mail(sender, recipients, subject, message):
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipients
    s = smtplib.SMTP(host=SMTP_SERVER_ADDRESS, port=SMTP_SERVER_PORT)
    with s:
        if SMTP_START_TLS:
            s.starttls()
        s.login(user=SMTP_USERNAME, password=SMTP_PASSWORD)
        s.send_message(msg)
