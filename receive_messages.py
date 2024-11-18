import boto3
import os
from dotenv import load_dotenv, dotenv_values
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

load_dotenv()

def receive_messages(queue_url, max_messages=1, wait_time=20):
    print("Initializing SQS client...")
    sqs = boto3.client('sqs', region_name=os.getenv("REGION"))

    try:
        print("Receiving messages...")
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time
        )
        messages = response.get('Messages', [])

        if not messages:
            print("No messages received.")
            return

        for message in messages:
            print(f"Received Message: {message['Body']}")

            # Delete message
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
            print("Message deleted successfully.")

    except (NoCredentialsError, PartialCredentialsError):
        print("AWS credentials not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    QUEUE_URL = os.getenv("QUEUE_URL")
    receive_messages(QUEUE_URL)
