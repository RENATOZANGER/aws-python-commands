from config.aws_config import get_session
from botocore.exceptions import ClientError


def list_athena_databases(client, catalog='AwsDataCatalog'):
    """
    Lists the databases in the specified Athena catalog.
    """
    try:
        response = client.list_databases(CatalogName=catalog)
        return response.get('DatabaseList', [])
    except ClientError as e:
        error_code = e.response['Error'].get('Code', 'Unknown')
        error_message = e.response['Error'].get('Message', str(e))
        print(f"❌ Error listing databases: {error_code} - {error_message}")
        return []


if __name__ == "__main__":
    databases = list_athena_databases(get_session().client('athena'))

    if not databases:
        print("No database found or an error occurred.")
    else:
        print("Databases in Athena:")
        for db in databases:
            print(f"Name: {db.get('Name')}, Description: {db.get('Description', 'No description')}")
