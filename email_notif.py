import smtplib
from email.mime.text import MIMEText

def send_email_notification(subject, message):
    gmail_user = "create new email"
    gmail_app_password = "ruos tjcu osep xdfb" #CREATE NEW TOKEN
    
    recipient = "add email recipient"
    
    msg = MIMEText(message)
    msg['From'] = gmail_user
    msg['To'] = recipient
    msg['Subject'] = subject
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, gmail_app_password)
            server.send_message(msg)
        print("✓ Email sent!")
    except Exception as e:
        print(f"✗ Error: {e}")

send_email_notification(
    subject="🤖 Script Finished!",
    message="A driver is driving. Here is the link : http://localhost:8501"
)