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

    # Peek at the next message in the queue without removing it
    messages = queue_client.peek_messages()
    for message in messages:
        decoded_content = base64.b64decode(message.content)
        print(f"Peeked message: {decoded_content}")

    # Receive and delete the next message from the queue
    messages = queue_client.receive_messages()
    for message in messages:
        print(f"Received message: {message.content}")

    # You can process the message content here

    # After processing, delete the message from the queue
    #queue_client.delete_message(message.id, message.pop_receipt)

addMessagetoQueue()