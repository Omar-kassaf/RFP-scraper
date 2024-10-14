import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from remove_csv_and_xlsx_files import remove_csv_and_xlsx_files

def send_email_without_results(to_addresses, subject, body):
    # Set up the email server and login credentials
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    email_address = "omarkamalabuassaf1@gmail.com"
    email_password = os.getenv('EMAIL_PASSWORD')

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = ", ".join(to_addresses)  
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'plain'))

    # Connect to Gmail server and send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_address, email_password)
    text = msg.as_string()
    server.sendmail(email_address, to_addresses, text)

    server.quit()
    remove_csv_and_xlsx_files()

    print('Email sent successfully!')