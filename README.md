# Smishing Campaign Script

This Python script sends simulated smishing messages to a list of employees for internal security awareness training. It reads a CSV file containing employee information and sends personalized messages using the [Textbelt](https://textbelt.com) SMS API.

---

## ⚠️ Disclaimer

**This script is intended for ethical use only**—e.g., internal phishing simulation campaigns authorized by your organization’s cybersecurity team. Do not use this for illegal or unauthorized activity.

---

## Features

- Sends personalized phishing-style SMS messages to a list of phone numbers.
- Encodes email addresses in phishing links using Base64.
- Uses a secure `.env` file for API key storage.
- Easy integration with the Textbelt SMS API.

---

## Prerequisites

- Python 3.7+
- A `.env` file with your `API_KEY`
- [Textbelt](https://textbelt.com) account (free test mode available)
- CSV file with columns: `name`, `number`, `email`

---

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/alicmc/SmishingTest.git
   cd SmishingTest
   ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Create a .env file in the root directory:
    ```
    API_KEY=your_textbelt_api_key
    ```
4. Prepare your CSV file:
    ```
    name,number,email
    John Doe,5551234567,john@example.com
    Jane Smith,5559876543,jane@example.com
    ```

## Usage

To run the campaign:
```
python smishing.py
```
When prompted, enter the path to your CSV file.

**Note**: By default, the script only prints the messages. To actually send messages, uncomment the line in `send_campaign()`:
```
# send_text(person['number'], message)
```
Be sure to modify the domain and message to suit your own needs.

## Example Output

```
[HR Reminder] Please review and confirm your contact details by July 15 to ensure our records are up to date. Access your HR portal here: hr.mycompany.com/am9obi5kb2VAZXhhbXBsZS5jb20=
```

## Security Tips

* Use _test mode while testing with Textbelt.
    * Don't get out of test mode unless you're 100% sure you want to send the message since it costs credits
* Do not store sensitive production keys in code.
* Log recipient interactions (if applicable) responsibly and ethically.