from config.aws_config import get_session


def get_account_id(client):
    """
    Retrieves the AWS account ID of the current session.
    """
    try:
        response = client.get_caller_identity()
        account_id = response['Account']
        return account_id
    except Exception as e:
        print(f"❌ Error retrieving account ID: {e}")
        return None
    

if __name__ == "__main__":
    sts_client = get_session().client('sts')
    account_id = get_account_id(sts_client)
    if account_id:
        print(f"Account ID: {account_id}")
    else:
        print("Failed to retrieve account ID.")
