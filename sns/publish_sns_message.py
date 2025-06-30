from config.aws_config import get_session


def publish_sns_message(sns_client, topic_arn: str, message: str,
                        subject: str = None, message_attributes: dict = None):
    """
    Publish a message to an SNS topic.
    """
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject,
        MessageAttributes=message_attributes or {},
    )
    return response


if __name__ == "__main__":
    sns_client = get_session().client('sns')
    topic_arn = 'arn:aws:sns:us-east-1:123456789012:MyTopic'
    message = 'Hello, this is a test message!'
    subject = 'Test Subject'
    message_attributes = {
        'Attribute1': {
            'DataType': 'String',
            'StringValue': 'Value1'
        },
        'Attribute2': {
            'DataType': 'Number',
            'StringValue': '123'
        }
    }

    response = publish_sns_message(sns_client, topic_arn, message, subject, message_attributes)
    print(f"Message published with ID: {response['MessageId']}")
