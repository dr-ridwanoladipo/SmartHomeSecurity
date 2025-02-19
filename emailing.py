import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage
from PIL import Image

# Load environment variables
load_dotenv()

SENDER = os.getenv("SENDER")
PASSWORD = os.getenv("PASSWORD")
RECEIVER = os.getenv("RECEIVER")


def get_image_subtype(image_path):
    """Determine the subtype of the image"""
    with open(image_path, "rb") as file:
        image = Image.open(file)
        return image.format.lower()


def send_email(image_path):
    """Send an email with the image attached"""
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we just saw a new customer!")

    # Attach the image
    with open(image_path, "rb") as file:
        content = file.read()
    image_subtype = get_image_subtype(image_path)
    email_message.add_attachment(content, maintype="images", subtype=image_subtype)

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as gmail:
            gmail.login(SENDER, PASSWORD)
            gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    send_email(image_path="images/51.png")