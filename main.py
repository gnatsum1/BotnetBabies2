"""
DISCLAIMER: This script is for educational and demonstration purposes only.
Do not use this script for any illegal, unethical, or harmful activities.
All templates and outputs are simulated and should not be used for real-world attacks or social engineering.

Tip: The 'Send Emails' button in the HTML UI does not actually send emails. It is for demonstration only. Integrate with a backend to enable real sending.
"""



import pandas
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

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
    "Attention: Your package is being held at customs due to missing information. "
    "To release your package and avoid return or additional charges, please visit the following link: {link}\n"
    "You may also scan the following QR code to resolve the issue: [QR CODE]\n"
    "Failure to respond within 24 hours may result in additional fees."
)

def render_preview(to_email, subject, body):
    print("\n--- Email Preview ---")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print("Body:")
    print(body)
    print("--- End Preview ---\n")

def is_valid_filename(filename):
    return bool(re.match(r'^[\w,\s-]+\.csv$', filename))

def is_valid_email(email):
    email = email.strip()
    return bool(re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email))

def sanitize_context(context):
    # Remove non-printable ASCII characters
    return re.sub(r'[^\x20-\x7E]', '', context)

def export_previews(previews, format):
    if format == 'html':
        html = '<html><body>'
        for p in previews:
            html += f"<b>To:</b> {p['to']}<br>"
            html += f"<b>Subject:</b> {p['subject']}<br>"
            html += f"<b>Body:</b><br> {p['body']}"
            if p['context']:
                html += f"<br><br>{p['context']}"
            # Add two empty lines before MITRE tag
            html += '<br><br>'
            if p['tags']:
                html += f"<b>Threat Tags:</b> <span style='color:#b00'>{', '.join(p['tags'])}</span>"
            html += '<hr>'
        html += '</body></html>'
        with open('email_previews.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print('Exported previews to email_previews.html')
    elif format == 'json':
        import json
        with open('email_previews.json', 'w', encoding='utf-8') as f:
            json.dump(previews, f, indent=2)
        print('Exported previews to email_previews.json')
    elif format == 'pdf':
        c = canvas.Canvas('email_previews.pdf', pagesize=letter)
        width, height = letter
        margin_left = 40
        margin_right = width - 40
        max_width = margin_right - margin_left
        y = height - 40
        for p in previews:
            c.setFont('Helvetica', 12)
            c.drawString(margin_left, y, f"To: {p['to']}")
            y -= 18
            c.drawString(margin_left, y, f"Subject: {p['subject']}")
            y -= 18
            c.drawString(margin_left, y, "Body:")
            y -= 18
            body_lines = simpleSplit(p['body'], 'Helvetica', 12, max_width)
            for line in body_lines:
                c.drawString(margin_left, y, line)
                y -= 14
            if p['context']:
                context_lines = simpleSplit(p['context'], 'Helvetica', 12, max_width)
                for line in context_lines:
                    c.drawString(margin_left, y, line)
                    y -= 14
            # Add empty line before MITRE tag
            y -= 14
            if p['tags']:
                c.setFillColorRGB(0.7,0,0)
                tags_line = f"Threat Tags: {', '.join(p['tags'])}"
                tags_lines = simpleSplit(tags_line, 'Helvetica', 12, max_width)
                for line in tags_lines:
                    c.drawString(margin_left, y, line)
                    y -= 18
                c.setFillColorRGB(0,0,0)
            c.line(margin_left, y, margin_right, y)
            y -= 24
            if y < 60:
                c.showPage()
                y = height - 40
        c.save()
        print('Exported previews to email_previews.pdf')

def send_campaign(filename, template_choice, context=None, only_emails=None, export_format=None):
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

    # Select template
    if template_choice == "hr":
        chosen_subject = subject
        chosen_body = body
        chosen_tags = [
            "Phishing: Spearphishing via Service (T1194)",
            "Impersonation: HR Department"
        ]
    elif template_choice == "tow":
        chosen_subject = tow_warning_subject
        chosen_body = tow_warning_body
        chosen_tags = [
            "Phishing: Spearphishing via Service (T1194)",
            "Urgency/Threat: Immediate Action Required",
            "Pretext: Vehicle Violation"
        ]
    elif template_choice == "customs":
        chosen_subject = customs_subject
        chosen_body = customs_body
        chosen_tags = [
            "Phishing: Spearphishing via Service (T1194)",
            "Pretext: Delivery/Logistics",
            "Impersonation: Customs/Shipping"
        ]
    else:
        print("Invalid template choice. Using default HR Reminder.")
        chosen_subject = subject
        chosen_body = body
        chosen_tags = [
            "Phishing: Spearphishing via Service (T1194)",
            "Impersonation: HR Department"
        ]

    def should_send(email):
        if only_emails is not None:
            return email in only_emails
        return True

    previews = []
    for index, row in df.iterrows():
        person = row.to_dict()
        email = person.get('email', '').strip()
        if not is_valid_email(email):
            print(f"Skipping invalid email: {email}")
            continue
        if not should_send(email):
            continue
        # Consistent formatting for all templates
        personalized_body = chosen_body
        personalized_subject = chosen_subject
        if context:
            personalized_body = f"{chosen_body}\n\n{context}"
        render_preview(email, personalized_subject, personalized_body)
        # Show MITRE tags after preview, not in email body
        if chosen_tags:
            print(f"Threat Tags: {', '.join(chosen_tags)}\n")
        send_email(email, personalized_subject, personalized_body)
        previews.append({
            'to': email,
            'subject': personalized_subject,
            'body': chosen_body,
            'context': context,
            'tags': chosen_tags
        })
    if export_format:
        export_previews(previews, export_format)

def send_email(to_email, subject, message):
    pass  # Output is already shown in render_preview; no need to repeat

def main():
    filename = input("Please input a valid .csv filename: ").strip()
    try:
        df = pandas.read_csv(filename)
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    emails = [row['email'].strip() for _, row in df.iterrows() if is_valid_email(row.get('email', '').strip())]
    if not emails:
        print("No valid emails found in the file.")
        return
    print("Possible recipients:")
    for idx, email in enumerate(emails, 1):
        print(f"{idx}. {email}")
    selected = input("Enter recipient numbers separated by commas (e.g. 1,3): ").strip()
    selected_indices = set()
    for part in selected.split(','):
        part = part.strip()
        if part.isdigit():
            idx = int(part)
            if 1 <= idx <= len(emails):
                selected_indices.add(idx-1)
    chosen_emails = [emails[i] for i in sorted(selected_indices)]
    if not chosen_emails:
        print("No valid recipients selected.")
        return
    print("Choose a template:")
    print("1. HR Reminder")
    print("2. Towing Warning")
    print("3. Customs Notice")
    num_choice = input("Enter template number (1/2/3): ").strip()
    if num_choice == "1":
        template_choice = "hr"
    elif num_choice == "2":
        template_choice = "tow"
    elif num_choice == "3":
        template_choice = "customs"
    else:
        print("Invalid choice. Using default HR Reminder.")
        template_choice = "hr"
    context = input("Enter any target details or context to tailor the message (or leave blank): ").strip()
    export_choice = input("Export previews? (none/html/json/pdf): ").strip().lower()
    export_format = export_choice if export_choice in ('html', 'json', 'pdf') else None
    send_campaign(filename, template_choice, context if context else None, only_emails=chosen_emails, export_format=export_format)

if __name__ == "__main__":
    main()