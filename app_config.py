import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    IMAP_HOST = os.getenv('imap_host')
    IMAP_USER = os.getenv('imap_user')
    IMAP_PASS = os.getenv('imap_pass')
    GMAIL_CLIENT_ID = os.getenv('client_id')
    GMAIL_CLIENT_SECRET = os.getenv('client_secret')
    GMAIL_PROJECT_ID = os.getenv('project_id')
    GMAIL_AUTH_URI = os.getenv('auth_uri')
    GMAIL_TOKEN_URI = os.getenv('token_uri')
    GMAIL_SCOPES = os.getenv('gmail_scopes')