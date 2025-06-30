from config.aws_config import get_session


def sqs_send_message_batch(sqs_client, queue_url, messages, delay_seconds=0):
    """
    Sends a batch of messages to an SQS queue.
    """
    try:
        entries = [
            {
                'Id': str(i),  # Unique ID for each message in the batch
                'MessageBody': message,
                'DelaySeconds': delay_seconds
            } for i, message in enumerate(messages)
        ]

        response = sqs_client.send_message_batch(
            QueueUrl=queue_url,
            Entries=entries
        )
        return response

    except Exception as e:
        print(f"❌ Error sending batch messages to SQS: {e}")
        return None


if __name__ == "__main__":
    sqs_client = get_session().client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'
    messages = [
        "Hello, this is the first message!",
        "Hello, this is the second message!",
        "Hello, this is the third message!"
    ]

    response = sqs_send_message_batch(sqs_client, queue_url, messages)

    if response:
        print(f"✅ Batch messages sent successfully!")
        print(f"  - Successful: {response.get('Successful')}")
        print(f"  - Failed: {response.get('Failed')}")
    else:
        print("❌ Failed to send batch messages.")
