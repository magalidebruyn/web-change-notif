import os
import requests
import hashlib
import smtplib
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file (edit the example.env file in this repo)
load_dotenv()

# Configuration
urls = ['https://philosophy.berkeley.edu/courses/term/98', 'https://philosophy.berkeley.edu/courses/detail/1708']
# Update these URLs as needed/given preference
# Make sure to adapt the .env file (the values for the environmental variables EMAIL_FROM, EMAIL_TO, SMTP_USERNAME, SMTP_PASSWORD)
email_from = os.getenv("EMAIL_FROM")  
email_to = os.getenv("EMAIL_TO")
email_subject = "Philosophy Graduate Seminars details are up!" # Update based on the subject
smtp_server = "smtp.gmail.com" # Update based on email provider
smtp_port = 587
smtp_username = os.getenv("SMTP_USERNAME") 
smtp_password = os.getenv("SMTP_PASSWORD")
# Create a user agent to reduce chances of being detected as a bot by the website + being blocked
headers = {'User-Agent': 'Mozilla/5.0'}


def get_content_hash(url: str):
    """
    Get the content hash of a webpage.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX        
        html_content = response.text
    except requests.RequestException as e:
        print(f"Error fetching URL {url} content: {e}")
        return None
    try:
        # Get the HMTL content as a soup object
        soup = BeautifulSoup(html_content, 'html.parser')
        # Remove script or style elements (Javascript/CSS style content that's dynamic)
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        # Reconvert to text - only the text content of the webpage
        cleaned_text = soup.get_text()
        # Hash
        hash_object = hashlib.md5(cleaned_text.encode())
        return hash_object.hexdigest()  
    except Exception as e:
        print(f"Error parsing HTML content into hash: {e}")
        return None  

def send_email(subject: str, body: str):
    """
    Send an email notification.
    """
    try: 
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            text = msg.as_string()
            server.sendmail(email_from, email_to, text)
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")

def main():
    # Retrieve the previous webpage(s) content/hash from a saved file
    try:
        with open('hash.txt', 'r') as file:
            previous_hash = file.read().strip()
    except FileNotFoundError:
        previous_hash = ''
    current_hash = ''
    # Get the current webpage(s) content/hash for each url
    for url in urls:
        print(f"{datetime.now()}: Retrieving url content from: {url}")
        hash_result = get_content_hash(url)
        if hash_result:
            current_hash += hash_result
        else:
            print(f"Skipping URL due to error: {url}")
    # Compare the previous content with the current content
    # Send email notification if it differs
    if current_hash != previous_hash:
        email_body = f"The content in the following webpage(s) has changed: {', '.join(urls)}"
        print(f"{datetime.now()}: The content in the following webpage(s) has changed: {', '.join(urls)}")
        send_email(email_subject, email_body)
        try:
            with open('hash.txt', 'w') as file:
                file.write(current_hash)
        except IOError as e:
            print(f"Error writing to hash.txt: {e}")


if __name__ == "__main__":
    main()
