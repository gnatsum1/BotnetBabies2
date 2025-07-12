import requests
import os
from dotenv import load_dotenv
import pandas

load_dotenv()  # load environment variables from .env file
api_key = os.environ.get('API_KEY', 'textbelt')


"""Send a smishing campaign to a group of people defined in a csv file.

filename: a csv file containing information in the format name,number,email
"""
def send_campaign(filename):
    df = pandas.read_csv(filename)
    print(df)
    for index, row in df.iterrows():
        person = row.to_dict()
        send_text(person['number'], person['name'])
        

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
    filename = input("Please input a valid .csv filename: ")
    send_campaign(filename)


if __name__ == "__main__":
    main()