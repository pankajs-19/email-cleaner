from imap_tools import MailBox, AND
from loguru import logger
from app_config import Config


def get_mails(from_date=None, end_date=None, batch_size=10):
    try:
        logger.info("Connecting to IMAP server...")
        messages = {'data': [], 'metadata': []}
        with MailBox(Config.IMAP_HOST).login(Config.IMAP_USER, Config.IMAP_PASS, "Inbox") as mailbox:
            msgs = mailbox.fetch(AND(body='unsubscribe'), reverse=True, mark_seen=False, limit=batch_size)
            for msg in msgs:
                data = {
                    'from': msg.from_,
                    'date': msg.date, 
                    'subject': msg.subject,
                    'body': msg.html or msg.text
                    }
                messages['data'].append(data)

            messages['metadata'].append({"total_count": len(messages['data'])})
            
        logger.info(f"Fetched {len(messages['data'])} messages.")
        return messages
    except Exception as e:
        logger.error(f"Failed to fetch emails: {e}")
        return {'error': str(e)}