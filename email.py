import time
import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

'''

    Created by Volkan EFE 03.06.2023

'''

def send_email_with_attachment(sender_email, sender_password, subject, body, attachment_path, recipient_email):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        html_body = f'''
        <html>
        <head></head>
        <body>
            <p>{body}</p>
        </body>
        </html>
        '''

        msg.attach(MIMEText(html_body, 'html'))

        attachment = open(attachment_path, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % attachment_path)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        print("Email sent successfully to", recipient_email)
    except Exception as e:
        print("An error occurred while sending the email to", recipient_email)
        print("Error details:", str(e))

def send_emails_from_csv(sender_email, sender_password, subject, body, attachment_path, csv_file_path, delay_seconds):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            recipient_email = row[0]
            time.sleep(delay_seconds)  # Delay for specified seconds
            send_email_with_attachment(sender_email, sender_password, subject, body, attachment_path, recipient_email)

# Usage example
sender_email = "your_email@gmail.com"
sender_password = "your_password"
subject = "Email subject"
body = "<h1>Hello World!</h1><p>Hi! This is test message!</p>"
attachment_path = "file.txt"
csv_file_path = "file.csv"
delay_seconds = 20

send_emails_from_csv(sender_email, sender_password, subject, body, attachment_path, csv_file_path, delay_seconds)
