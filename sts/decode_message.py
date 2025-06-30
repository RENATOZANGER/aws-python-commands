from config.aws_config import get_session
from botocore.exceptions import ClientError, BotoCoreError


def decode_message(client,encoded_message):
    """
    Decodes an authorization message that has been encoded.
    """
    try:
        response = client.decode_authorization_message(
            EncodedMessage=encoded_message
        )
        decoded_message = response.get('DecodedMessage', 'No message decoded')
        print(f"✅ Decoded message: {decoded_message}")
        return decoded_message
    except ClientError as e:
        print(f"❌ Error decoding message: {e}")
    except BotoCoreError as e:
        print(f"❌ BotoCore error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    sts_client = get_session().client('sts')
    encoded_message = "your_encoded_message_here"
    
    decode_message(sts_client, encoded_message)
