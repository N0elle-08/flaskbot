import os
import logging

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD") 
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_SCHEMA = os.environ.get("DB_SCHEMA")

# # Configuration
# cloudinary.config(
#   cloud_name = os.environ.get("CLOUD_NAME"),
#   api_key = os.environ.get("API_KEY"),
#   api_secret = os.environ.get("API_SECRET")
# )
def setup_logger():
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.DEBUG)
    
    # Avoid adding multiple handlers if the logger already has handlers
    if not logger.hasHandlers():
        fh = logging.FileHandler('debug.log', mode='w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
