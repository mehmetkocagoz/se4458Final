from azure.storage.queue import QueueServiceClient
import base64
from dotenv import load_dotenv
import os

load_dotenv()

# Replace these with your actual values
account_name = os.getenv('AZURE_ACCOUNT_NAME')
account_key = os.getenv('AZURE_ACCOUNT_KEY')
queue_name = os.getenv('QUEUE_NAME')

def connect():
    # Create a QueueServiceClient
    queue_service_client = QueueServiceClient(account_url=f"https://{account_name}.queue.core.windows.net", credential=account_key)

    # Create a QueueClient
    queue_client = queue_service_client.get_queue_client(queue_name)

    return queue_client

def addMessagetoQueue(jsonFormatMessage):
    queue_client = connect()

    # Encode the message content (assuming it's a string)
    encoded_message = base64.b64encode(jsonFormatMessage.encode()).decode('utf-8')
    queue_client.send_message(encoded_message)
    