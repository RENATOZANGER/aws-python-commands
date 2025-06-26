from botocore.exceptions import ClientError
from config.aws_config import get_session



def download_file_s3(s3_client, bucket_name: str, file_path: str, local_file_path: str = None):
    """
    Downloads a file from an S3 bucket to a local path.
    
    If `local_file_path` is not provided, it will use the same name as the file in S3.
    """
    try:
        if local_file_path is None:
            local_file_path = file_path.split('/')[-1]  # Use the last part of the S3 path as the local file name
        
        print(f"📥 Downloading from s3://{bucket_name}/{file_path} to {local_file_path}")
        s3_client.download_file(bucket_name, file_path, local_file_path)
        print("✅ Download completed.")
    
    except ClientError as e:
        error_code = e.response['Error'].get('Code', 'Unknown')
        print(f"❌ Error accessing object in S3: {error_code} - {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        

if __name__ == "__main__":
    s3_client = get_session().client('s3')
    bucket_name = 'your-bucket-name'
    file_path = 'path/to/your/file/in/s3'
    local_file_path = 'desired/local/file/path'  # Optional, can be None to use default name

    download_file_s3(s3_client, bucket_name, file_path, local_file_path)
