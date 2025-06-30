from config.aws_config import get_session
from botocore.exceptions import ClientError, BotoCoreError

def process_sqs_message(sqs_client, queue_url):
    """
    Receives and processes a single message from an SQS queue.
    After processing, deletes the message from the queue.
    """
    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        if 'Messages' in response:
            for msg in response['Messages']:
                print(f"📥 Message received: {msg['Body']}")

                # Delete the message after processing
                sqs_client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=msg['ReceiptHandle']
                )
                print(f"🗑️ Message deleted: {msg['MessageId']}")
        else:
            print("No messages available at the moment.")

    except (ClientError, BotoCoreError) as e:
        print(f"❌ Error processing SQS messages: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    sqs_client = get_session().client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'
    process_sqs_message(sqs_client, queue_url)
