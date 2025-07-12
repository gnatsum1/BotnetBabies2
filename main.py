import requests
import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file
api_key = os.environ.get('API_KEY')

"""Send a single text message using the Textbelt API.

number: a string containing a standard 10-digit phone number.
message: the message you would like to send.
"""
def send_text(number, message):
    resp = requests.post('https://textbelt.com/text', {
    'phone': number,
    'message': message,
    'key': api_key + '_test'
    })
    print(resp.json())

def main():
    send_text(input(), 'hi hello')

if __name__ == "__main__":
    main()