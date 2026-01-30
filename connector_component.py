import base64
from loguru import logger
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from connector_helpers import convert_to_date

SERVICE_CACHE = {}

def get_gmail_service(creds):
    key = creds.token
    if key not in SERVICE_CACHE:
        SERVICE_CACHE[key] = build("gmail", "v1", credentials=creds)
    return SERVICE_CACHE[key]

def extract_body_from_payload(payload):
    try:
        if payload.get("mimeType") == "text/html":
            data = payload.get("body", {}).get("data")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8")

        for part in payload.get("parts", []):
            body = extract_body_from_payload(part)
            if body:
                return body

        return ""
    except Exception as e:
        logger.error(f"Error extracting body from payload: {str(e)}")
        return ""


def get_mail_body(creds, message_id):
    """Helper to extract body text from complex nested Gmail payloads."""
    try:
        service = get_gmail_service(creds)

        msg = service.users().messages().get(
            userId="me",
            id=message_id,
            format="full"
        ).execute()

        payload = msg.get("payload",{})
        body = extract_body_from_payload(payload)
        
        response = {"body": body}
        return response
    
    except Exception as e:
        logger.error(f"Error extracting body from payload: {str(e)}")
        return ""

def list_mail_messages(creds, from_date=None, end_date=None, batch_size=None):
    try:
        service = get_gmail_service(creds)
        query_parts = ['+:unsubscribe']

        logger.info("Gmail API service initialized.")
        
        if from_date and end_date:
            # Gmail uses YYYY/MM/DD format
            from_date_dt = convert_to_date(from_date)
            query_parts.append(f"after:{from_date_dt.strftime('%Y/%m/%d')}")
            end_date_dt = convert_to_date(end_date) + timedelta(days=1)
            query_parts.append(f"before:{end_date_dt.strftime('%Y/%m/%d')}")
        
        else:
            # last 7 days by default
            default_from_date = (datetime.now() - timedelta(days=7)).strftime('%Y/%m/%d')
            query_parts.append(f"after:{default_from_date}")
            default_end_date = (datetime.now() + timedelta(days=1)).strftime('%Y/%m/%d')
            query_parts.append(f"before:{default_end_date}")
        
        logger.info(f"Querying gmail API: {query_parts}")

        search_query = " ".join(query_parts)
        params = {
            "userId": "me",
            "q": search_query,
            "maxResults": batch_size or 50
        }

        results = service.users().messages().list(**params).execute()

        messages  = []

        for msg_meta in results.get("messages", []):
            msg = service.users().messages().get(
                userId='me', 
                id=msg_meta['id'],
                format="metadata",
                metadataHeaders=["Subject", "From", "Date"]
                ).execute()
            
            payload = msg.get("payload", {})
            headers = payload.get('headers', [])
            
            # Extract header info
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
            from_email = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown")
            date_str = next((h['value'] for h in headers if h['name'] == 'Date'), "")

            messages.append({
                "id": msg_meta["id"],
                'from': from_email,
                'date': date_str,
                'subject': subject,
                "snippet": msg.get("snippet", "")
            })

        logger.info(f"Fetched {len(messages)} messages via API.")
        return messages

    except Exception as e:
        logger.error(f"Failed to fetch emails via Gmail API: {str(e)}")
        return {'error': str(e)}