from config.aws_config import get_session


def get_object_metadata(s3_client, bucket_name: str, object_key: str):
    """
    Retrieves metadata of an object in an S3 bucket.
    """
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        for key, value in response.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Failed to retrieve metadata for {object_key} in {bucket_name}: {e}")
        raise e
    

if __name__ == "__main__":
    s3_client = get_session().client('s3')
    bucket_name = 'your-bucket-name'
    object_key = 'path/to/your/object'
    metadata = get_object_metadata(s3_client, bucket_name, object_key)
