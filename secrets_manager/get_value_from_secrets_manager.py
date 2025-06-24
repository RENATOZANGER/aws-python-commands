from config.aws_config import get_session

def get_value_from_secrets_manager(client, secret_name: str) -> str | None:
    """
    Retrieves a value from AWS Secrets Manager.
    """
    try:
        response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            return response['SecretString']
        else:
            print(f"❌ Secret {secret_name} does not contain a string value.")
            return None
    except Exception as e:
        print(f"❌ Error retrieving secret {secret_name}: {e}")
        return None

if __name__ == "__main__":
    secrets_client = get_session().client('secretsmanager')
    secret_name = 'my_secret_name'  # Replace with your secret name

    secret_value = get_value_from_secrets_manager(secrets_client, secret_name)

    if secret_value:
        print(f"Value of secret '{secret_name}': {secret_value}")
    else:
        print(f"Failed to retrieve value for secret '{secret_name}'.")
