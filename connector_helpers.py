from loguru import logger
from datetime import datetime

def convert_to_date(date_str):
    """Convert a date string in 'YYYY-MM-DD' format to a datetime object."""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        return date
    except ValueError as e:
        logger.error(f"Date conversion error: {str(e)}")
        return None