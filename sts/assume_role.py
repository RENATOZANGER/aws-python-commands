import boto3
from config.aws_config import get_session


def assume_role(sts_client, role_arn, role_session_name, region_name='us-east-1'):
  """ assume_role function. """
  try:
    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )
    return response['Credentials']
  except Exception as e:
    print(f"Error assuming role: {e}")
    return None

if __name__ == "__main__":
    role_arn = "arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_ROLE_NAME"
    role_session_name = "MySession"
    session = get_session()
    sts_client = session.client('sts')
    credentials = assume_role(sts_client, role_arn, role_session_name)
    
    if credentials:
        print(f"  Access Key ID: {credentials['AccessKeyId']}")
        print(f"  Secret Access Key: {credentials['SecretAccessKey']}")
        print(f"  Session Token: {credentials['SessionToken']}")
        print(f"  Expiration: {credentials['Expiration']}")
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
        )
        try:
            response = s3_client.list_buckets()
            print("List buckets (using default credentials):")
            for bucket in response['Buckets']:
                print(f"  - {bucket['Name']}")
        except Exception as e:
            print(f"Error listing buckets: {e}")
