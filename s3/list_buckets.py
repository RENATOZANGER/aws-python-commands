from config.aws_config import get_session


def list_buckets(s3_client):
    """
    Lists all S3 buckets in the AWS account
    """
    response = s3_client.list_buckets()
    for bucket in response['Buckets']:
        print(bucket['Name'])


if __name__ == "__main__":
    s3_client = get_session().client('s3')
    list_buckets(s3_client)
