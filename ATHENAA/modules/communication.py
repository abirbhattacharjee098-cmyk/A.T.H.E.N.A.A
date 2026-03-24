import smtplib
from email.message import EmailMessage
import imaplib
import email
import pywhatkit
from datetime import datetime

class CommunicationSystem:
    def __init__(self, config=None):
        self.config = config

    def send_email(self, to_addr: str, subject: str, body: str):
        """Send an email."""
        if not self.config:
            return False, "Configuration not found."
            
        email_config = self.config.get("email", {})
        sender = email_config.get("address")
        password = email_config.get("password")
        smtp_server = email_config.get("smtp_server", "smtp.gmail.com")
        
        if not sender or not password or password == "your_app_password":
            return False, "Email credentials not configured properly in config.json."
            
        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = to_addr
            msg.set_content(body)

            with smtplib.SMTP_SSL(smtp_server, 465) as smtp:
                smtp.login(sender, password)
                smtp.send_message(msg)
            return True, f"Email sent to {to_addr}"
        except Exception as e:
            return False, f"Failed to send email: {e}"

    def send_whatsapp(self, number: str, message: str):
        """Send WhatsApp message using pywhatkit."""
        try:
            # Assumes the number includes country code e.g. +1234567890
            now = datetime.now()
            # Send message in 1 minute from now to give time for whatsapp web to load
            hour = now.hour
            minute = now.minute + 1
            if minute == 60:
                minute = 0
                hour = (hour + 1) % 24
                
            pywhatkit.sendwhatmsg(number, message, hour, minute, wait_time=15, tab_close=True, close_time=3)
            return True, f"Scheduled WhatsApp message to {number}"
        except Exception as e:
            return False, f"Failed to send WhatsApp message: {e}"
