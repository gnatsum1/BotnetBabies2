"""
DISCLAIMER: This script is for educational and demonstration purposes only.
Do not use this script for any illegal, unethical, or harmful activities.
All templates and outputs are simulated and should not be used for real-world attacks or social engineering.

WARNING: The script is now configured to send real emails using SMTP. Use with caution and only with explicit permission from all recipients.
"""

import os
import pandas
import re
from email.mime.text import MIMEText
from dotenv import load_dotenv
import smtplib

load_dotenv()  # load environment variables from .env file
smtp_server = os.environ.get('SMTP_SERVER', 'smtp.example.com')
smtp_port = int(os.environ.get('SMTP_PORT', 587))
smtp_user = os.environ.get('SMTP_USER', 'user@example.com')
smtp_password = os.environ.get('SMTP_PASSWORD', 'password')
from_email = os.environ.get('FROM_EMAIL', smtp_user)
subject = "HR Reminder: Confirm Your Contact Details"
body = "Please review and confirm your contact details by July 15 to ensure our records are up to date."

# Additional phishing templates
tow_warning_subject = "Urgent: Vehicle Towing Notice"
tow_warning_body = (
    "Attention: Your vehicle is scheduled for towing due to a parking violation. "
    "To avoid immediate towing and resolve this issue, please visit the following link: {link}\n"
    "Failure to respond within 24 hours may result in additional fees."
)

customs_subject = "Action Required: Package Held at Customs"
customs_body = (
    "Dear Customer,\n\n"
    "Your package is currently being held at customs due to missing information. "
    "To release your package and avoid return or additional charges, please complete the required form at the following link: {link}\n\n"
    "Thank you for your prompt attention."
)



"""Send an email campaign to a group of people defined in a csv file.

filename: a csv file containing information in the format name,number,email.
"""
def render_preview(to_email, subject, body):
    print("\n--- Email Preview ---")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print("Body:")
    print(body)
    print("--- End Preview ---\n")

def is_valid_filename(filename):
    # Only allow .csv files, no path traversal
    return bool(re.match(r'^[\w,\s-]+\.csv$', filename))

def is_valid_email(email):
    # Basic email validation
    return bool(re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email))

def sanitize_context(context):
    # Remove potentially dangerous characters
    return re.sub(r'[^\w\s.,:;!?@#\-]', '', context)

def send_campaign(filename, context=None):
    if not is_valid_filename(filename):
        print("Invalid filename. Only .csv files in the current directory are allowed.")
        return
    try:
        df = pandas.read_csv(filename)
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    print(df)
    if context:
        context = sanitize_context(context)
    for index, row in df.iterrows():
        person = row.to_dict()
        email = person.get('email', '')
        if not is_valid_email(email):
            print(f"Skipping invalid email: {email}")
            continue
        # Choose template and personalize
        personalized_body = body
        personalized_subject = subject
        if context:
            personalized_body = body + f"\n\nContext: {context}"
        render_preview(email, personalized_subject, personalized_body)
        send_email(email, personalized_subject, personalized_body)


"""Send a single email using SMTP.

to_email: recipient's email address.
subject: email subject.
message: email body.
"""
def send_email(to_email, subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, [to_email], msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")


def main():
    filename = input("Please input a valid .csv filename: ").strip()
    context = input("Enter any target details or context to tailor the message (or leave blank): ").strip()
    send_campaign(filename, context if context else None)


if __name__ == "__main__":
    main()