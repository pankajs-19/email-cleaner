import os
from loguru import logger
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from app_config import Config

SCOPES = [Config.GMAIL_SCOPES]

class AuthMgmt:
    credentials = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AuthMgmt, cls).__new__(cls)
        return cls.instance
    
    def get_credentials(self):
        try:
            logger.info("Obtaining Gmail API credentials...")

            if self.credentials and self.credentials.valid:
                return self.credentials

            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
                return self.credentials

            # 2. Reconstruct the Client Config from .env instead of a file
            client_config = {
                "installed": {
                    "client_id": Config.GMAIL_CLIENT_ID,
                    "client_secret": Config.GMAIL_CLIENT_SECRET,
                    "project_id": Config.GMAIL_PROJECT_ID,
                    "auth_uri": Config.GMAIL_AUTH_URI,
                    "token_uri": Config.GMAIL_TOKEN_URI,
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "redirect_uris": ["http://localhost"]
                }
            }
            
            # 3. Use 'from_client_config' instead of 'from_client_secrets_file'
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            self.credentials = flow.run_local_server(port=0)

            return self.credentials
        
        except Exception as e:
            logger.error(f"Error obtaining credentials: {str(e)}")