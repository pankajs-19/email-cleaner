import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    IMAP_HOST = os.getenv('imap_host')
    IMAP_USER = os.getenv('imap_user')
    IMAP_PASS = os.getenv('imap_pass')