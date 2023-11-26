from dotenv import load_dotenv
import os


def load_env():
    load_dotenv()
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    return client_id, client_secret
