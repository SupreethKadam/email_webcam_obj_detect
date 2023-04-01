import smtplib
import os
import imghdr
from email.message import EmailMessage

EMAIL_SENDER = "supreethkadam.itez@gmail.com"
PASSWORD = os.getenv("PASSWORD")
EMAIL_RECEIVER = "supreethkadam.itez@gmail.com"


def send_email(img_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New customer arrived!"
    email_message.set_content("Hey, we just saw a new customer.")

    with open(img_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(EMAIL_SENDER, PASSWORD)
    gmail.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email(img_path="images/1.png")
