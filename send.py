import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_FROM_ADDRESS = os.getenv("EMAIL_FROM_ADDRESS")
TEST_TO_EMAIL = "abhilashchutia1999@gmail.com" # Mailtrap will capture this regardless

if not all([EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_FROM_ADDRESS]):
    print("Email configuration incomplete. Check .env file.")
else:
    msg = MIMEText("This is a test email from your application.")
    msg["Subject"] = "Test Email from FastAPI App"
    msg["From"] = EMAIL_FROM_ADDRESS
    msg["To"] = TEST_TO_EMAIL

    try:
        print(f"Attempting to connect to {EMAIL_HOST}:{EMAIL_PORT}...")
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            print("Connection established. Starting TLS...")
            server.starttls()
            print("TLS started. Logging in...")
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            print("Login successful. Sending email...")
            server.send_message(msg)
            print(f"Test email sent to {TEST_TO_EMAIL}")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}. Check username/password.")
    except smtplib.SMTPConnectError as e:
        print(f"SMTP Connection Error: {e}. Check host/port/network.")
    except Exception as e:
        print(f"Failed to send test email: {e}")