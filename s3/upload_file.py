from botocore.exceptions import ClientError

from config.aws_config import get_session


def upload_file_s3(s3_client, bucket_name: str, file_path: str, object_name: str = None):
    """
    Uploads a file to an S3 bucket.
    """
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
    except ClientError as e:
        print(f"Failed to upload {file_path} to {bucket_name}/{object_name}: {e}")
        raise e
    

if __name__ == "__main__":
    s3_client = get_session().client('s3')
    file_path = 'path/to/your/file'
    bucket_name = 'your-bucket-name'
    object_name = 'desired/object/name/in/s3'
    upload_file_s3(s3_client, bucket_name, file_path, object_name)
