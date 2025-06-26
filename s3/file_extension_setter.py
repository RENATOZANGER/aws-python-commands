import mimetypes
from botocore.exceptions import ClientError, BotoCoreError
from config.aws_config import get_session


def set_file_extension_based_on_content_type(s3_client, bucket_name: str, file_path: str) -> None:
    """
    Set the file extension based on the content type of an object in S3 and download it.
    """
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=file_path)
        content_type = response.get('ContentType', '')
        if content_type:
            extension = mimetypes.guess_extension(content_type)
            if extension and not file_path.endswith(extension):
                new_file_path = f"{file_path}{extension}"
            else:
                new_file_path = file_path
        else:
            new_file_path = file_path
        
        print(f"📥 Downloading from s3://{bucket_name}/{file_path} for {new_file_path}")
        s3_client.download_file(bucket_name, file_path, new_file_path)
        print("✅ Download completed.")
    
    except ClientError as e:
        error_code = e.response['Error'].get('Code', 'Unknown')
        print(f"❌ Error accessing object in S3: {error_code} - {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    s3_client = get_session().client('s3')
    bucket_name = 'your-bucket-name'
    file_path = 'path/to/your/file'
    set_file_extension_based_on_content_type(s3_client, bucket_name, file_path)
