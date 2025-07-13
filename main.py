import requests
import os
from dotenv import load_dotenv
import pandas
import base64

load_dotenv()  # load environment variables from .env file
api_key = os.environ.get('API_KEY', 'textbelt')
url = "[domain]"
script = "[HR Reminder] Please review and confirm your contact details by July 15 to ensure our records are up to date. Access your HR portal here: "


"""Send a smishing campaign to a group of people defined in a csv file.

filename: a csv file containing information in the format name,number,email.
"""
def send_campaign(filename):
    df = pandas.read_csv(filename)
    print(df)
    for index, row in df.iterrows():
        person = row.to_dict()
        message = script + make_phishing_link(person['email'], url)
        print(message)
        # send_text(person['number'], message) # uncomment this line to send the message
        
"""Make a phishing link using a base64-encoded id.

id: a string used to identy a person (e.g. an email).
url: the base url.
"""
def make_phishing_link(id, url):
    encoded_id = base64.b64encode(id.encode('utf-8'))
    return url + '/' + encoded_id.decode('utf-8')


"""Send a single text message using the Textbelt API.

number: a string containing a standard 10-digit phone number.
message: the message you would like to send.
"""
def send_text(number, message):
    resp = requests.post('https://textbelt.com/text', {
    'phone': number,
    'message': message,
    'key': api_key + '_test' # only take it off test mode if you're ready to send it out
    })
    print(resp.json())


def main():
    filename = input("Please input a valid .csv filename: ")
    send_campaign(filename)


if __name__ == "__main__":
    main()