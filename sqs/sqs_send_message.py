from config.aws_config import get_session


def send_message_to_sqs(sqs_client, queue_url, message_body, delay_seconds=0):
    """
    Sends a message to an SQS queue.
    """
    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            DelaySeconds=delay_seconds
        )
        return response
    except Exception as e:
        print(f"❌ Error sending message to SQS: {e}")
        return None
    

if __name__ == "__main__":
    sqs_client = get_session().client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'
    message_body = 'Hello, this is a test message!'

    response = send_message_to_sqs(sqs_client, queue_url, message_body)

    if response:
        print(f"Message sent successfully! Message ID: {response['MessageId']}")
    else:
        print("Failed to send message.")
