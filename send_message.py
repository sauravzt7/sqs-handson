import boto3
import os
from dotenv import load_dotenv, dotenv_values
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


load_dotenv()


def send_message(queue_url, message_body):
    # Initialize SQS client
    sqs = boto3.client('sqs', region_name=os.getenv("REGION"))  # Replace with your region

    try:
        # Send message to SQS queue
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print(f"Message sent! ID: {response['MessageId']}")
    except (NoCredentialsError, PartialCredentialsError):
        print("AWS credentials not found. Please configure your credentials.")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    # Replace with your actual queue URL
    QUEUE_URL = os.getenv("QUEUE_URL")
    MESSAGE_BODY = 'Hello from VSCode and Boto3!'
    send_message(QUEUE_URL, MESSAGE_BODY)
