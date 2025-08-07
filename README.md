# Email Phishing Simulation App

This project provides a simple HTML front-end and Python backend for simulating email phishing campaigns for internal security awareness training. It allows you to preview and customize simulated phishing emails to selected recipients from a CSV file. No real emails are sent.

---

## ⚠️ Disclaimer

**This app is for ethical, educational, and authorized use only.** Do not use for illegal, unethical, or unauthorized activity. All templates and outputs are simulated and should not be used for real-world attacks or social engineering.

---

## Features

- Preview simulated phishing-style emails to selected recipients (no sending).
- Choose from multiple phishing templates (HR, towing, customs, etc.) with threat tagging (MITRE ATT&CK).
- Add custom context/details to personalize messages (context appears after the body and before threat tags in previews).
- Select individual recipients from your CSV file in the UI.
- Export previews as HTML, JSON, or PDF for offline use (UI and backend).
- HTML front-end for easy campaign setup and preview.
- Python backend for console-based preview (no sending).
- MITRE threat tags are shown in the preview only and are not part of the actual email body.

---

## Prerequisites

- Python 3.7+
- CSV file with columns: `name`, `number`, `email`
- Modern web browser (for HTML UI)
- `reportlab` Python package (for PDF export in backend)

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

3. Prepare your CSV file:
    ```
    name,number,email
    Alice Johnson,5551234567,alice.johnson@example.com
    Bob Smith,5552345678,bob.smith@example.com
    Carol Lee,5553456789,carol.lee@example.com
    David Kim,5554567890,david.kim@example.com
    Eve Martinez,5555678901,eve.martinez@example.com
    ```

---

## Usage

### Front-End (HTML UI)

1. Open `email_campaign_ui.html` in your web browser.
2. Select your CSV file, choose recipients, pick a template, and add context.
3. Click "Preview Emails" to see the simulated messages and threat tags (tags are not part of the email body).
4. Export previews as HTML, JSON, or PDF using the export buttons below the preview.
5. (Demo only) The UI does not send emails; integrate with the backend to enable sending.

### Backend (Python)

1. Run `main.py` in your terminal.
2. Follow prompts to select recipients, template, and context.
3. Previewed emails and threat tags will be shown in the console (tags are not part of the email body).
4. When prompted, choose to export previews as HTML, JSON, or PDF for offline use.
5. No emails are sent.

---

## Security Tips

- Never use this app for real-world phishing or malicious activity.
- Do not store sensitive production credentials in code or public repos.
- Log and handle recipient data responsibly and ethically.