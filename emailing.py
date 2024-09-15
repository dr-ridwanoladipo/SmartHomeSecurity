import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage
from PIL import Image

load_dotenv()

SENDER = os.getenv("SENDER")
PASSWORD = os.getenv("PASSWORD")
RECEIVER = os.getenv("RECEIVER")


def get_image_subtype(image_path):
    with open(image_path, "rb") as file:
        image = Image.open(file)
        return image.format.lower()


def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we just saw a new customer!")

    with open(image_path, "rb") as file:
        content = file.read()
    image_subtype = get_image_subtype(image_path)
    email_message.add_attachment(content, maintype="image", subtype=image_subtype)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as gmail:
            gmail.login(SENDER, PASSWORD)
            gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    send_email(image_path="images/51.png")
