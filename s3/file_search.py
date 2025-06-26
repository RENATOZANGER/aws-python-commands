from config.aws_config import get_session


def find_file_in_s3_bucket(s3_client, prefix: str, bucket_name: str, file_name: str):
    """
    Searches for a file in an S3 bucket and returns its key if found.
    """
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        file_found = ''
        if 'Contents' in response:
            for obj in response['Contents']:
                if file_name in obj['Key']:
                    file_found = obj['Key']
                    break
        if file_found:
            print(f"File {file_name} found in bucket {bucket_name}: {file_found}")
        else:
            print(f"File {file_name} not found in bucket {bucket_name} with prefix {prefix}")
    except Exception as e:
        print(f"Error searching for file {file_name} in bucket {bucket_name}: {e}")
        raise e
    

if __name__ == "__main__":
    s3_client = get_session().client('s3')
    bucket_name = 'your-bucket-name'
    prefix = 'your/prefix/'
    file_name = 'name_of_your_file'
    find_file_in_s3_bucket(s3_client, prefix, bucket_name, file_name)
