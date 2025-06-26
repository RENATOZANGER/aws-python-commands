from botocore.exceptions import ClientError
from config.aws_config import get_session


def delete_all_object_versions(s3_client, bucket_name: str, object_key: str):
    """
    delete_all_object_versions deletes all versions of a specific object in an S3 bucket.
    """
    try:
        paginator = s3_client.get_paginator('list_object_versions')
        for page in paginator.paginate(Bucket=bucket_name, Prefix=object_key):
            delete_items = []

            versions = page.get('Versions', [])
            delete_markers = page.get('DeleteMarkers', [])

            # Get all versions of the specified object
            for version in versions:
                if version['Key'] == object_key:
                    delete_items.append({
                        'Key': object_key,
                        'VersionId': version['VersionId']
                    })

            # Get all delete markers for the specified object
            for marker in delete_markers:
                if marker['Key'] == object_key:
                    delete_items.append({
                        'Key': object_key,
                        'VersionId': marker['VersionId']
                    })

            # delete the versions and delete markers
            if delete_items:
                response = s3_client.delete_objects(
                    Bucket=bucket_name,
                    Delete={'Objects': delete_items}
                )
                deleted = response.get('Deleted', [])
                for item in deleted:
                    print(f"✅ Deleted: {item['Key']} - Version: {item['VersionId']}")
            else:
                print("No versions found.")

    except ClientError as e:
        print(f"❌ Error deleting versions: {e}")


if __name__ == "__main__":
    s3_client = get_session().client('s3')
    bucket_name = 'your-bucket-name'
    object_key = 'path/file'
    delete_all_object_versions(s3_client, bucket_name, object_key)
