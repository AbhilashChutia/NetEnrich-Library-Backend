import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

# Get email configuration
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 2525))  # Mailtrap uses 2525
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_FROM_ADDRESS = os.getenv("EMAIL_FROM_ADDRESS")

def verify_email_config():
    print("Checking email configuration...")
    
    # Check if all required variables are set
    required_vars = {
        "EMAIL_HOST": EMAIL_HOST,
        "EMAIL_PORT": EMAIL_PORT,
        "EMAIL_USERNAME": EMAIL_USERNAME,
        "EMAIL_PASSWORD": EMAIL_PASSWORD,
        "EMAIL_FROM_ADDRESS": EMAIL_FROM_ADDRESS
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease create a .env file with these variables:")
        print("EMAIL_HOST=smtp.mailtrap.io")
        print("EMAIL_PORT=2525")
        print("EMAIL_USERNAME=your_mailtrap_username")
        print("EMAIL_PASSWORD=your_mailtrap_password")
        print("EMAIL_FROM_ADDRESS=library@yourdomain.com")
        return False
    
    print("✅ All required environment variables are set")
    
    # Verify Mailtrap configuration
    if EMAIL_HOST != "smtp.mailtrap.io":
        print(f"⚠️ Warning: EMAIL_HOST is set to {EMAIL_HOST}, expected smtp.mailtrap.io")
    
    if EMAIL_PORT != 2525:
        print(f"⚠️ Warning: EMAIL_PORT is set to {EMAIL_PORT}, expected 2525")
    
    return True

def test_smtp_connection():
    print("\nTesting SMTP connection to Mailtrap...")
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            print(f"✅ Successfully connected to {EMAIL_HOST}:{EMAIL_PORT}")
            
            # Enable TLS
            server.starttls()
            print("✅ TLS enabled")
            
            # Try to login
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            print("✅ SMTP authentication successful")
            
            # Create a test message
            msg = MIMEText("This is a test email to verify Mailtrap SMTP configuration.")
            msg["Subject"] = "Mailtrap SMTP Test"
            msg["From"] = EMAIL_FROM_ADDRESS
            msg["To"] = "test@example.com"
            
            # Try to send
            server.send_message(msg)
            print("✅ Test email sent successfully")
            print("\n📧 Check your Mailtrap inbox to see the test email!")
            return True
                
    except smtplib.SMTPConnectError as e:
        print(f"❌ Failed to connect to Mailtrap: {e}")
        print("Please verify your EMAIL_HOST and EMAIL_PORT settings")
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP authentication failed: {e}")
        print("Please verify your EMAIL_USERNAME and EMAIL_PASSWORD from Mailtrap")
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error occurred: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Please make sure you're using the correct Mailtrap credentials")
    
    return False

if __name__ == "__main__":
    if verify_email_config():
        test_smtp_connection() 