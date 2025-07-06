from config.aws_config import get_session


def get_aws_credentials(sts_client):
    """
    Retrieve temporary credentials.
    """
    try:
        response = sts_client.get_credentials().get_frozen_credentials()
        return response
    except Exception as e:
        print(f"❌ Error retrieving AWS credentials: {e}")
        return None


if __name__ == "__main__":
    sts_client = get_session().client('sts')
    credentials = sts_client.get_session_token(sts_client)
    if credentials:
        aws_credentials = get_aws_credentials(sts_client)
        if aws_credentials:
            print(f"AWS Access Key: {aws_credentials.access_key}")
            print(f"AWS Secret Key: {aws_credentials.secret_key}")
            print(f"AWS Session Token: {aws_credentials.token}")
        else:
            print("Failed to retrieve AWS credentials.")
    else:
        print("Failed to retrieve AWS credentials.")
