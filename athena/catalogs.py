from config.aws_config import get_session
from botocore.exceptions import ClientError


def list_athena_data_catalogs(client):
    """
    Lists the data catalogs in AWS Athena.
    """
    try:
        response = client.list_data_catalogs(client)
        return response.get('DataCatalogsSummary', [])
    except ClientError as e:
        error_code = e.response['Error'].get('Code', 'Unknown')
        error_message = e.response['Error'].get('Message', str(e))
        print(f"❌ Error listing data catalogs: {error_code} - {error_message}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error while listing data catalogs: {e}")
        return []


if __name__ == "__main__":
    catalogs = list_athena_data_catalogs(get_session().client('athena'))

    if not catalogs:
        print("No catalog found or an error occurred.")
    else:
        print("Data Catalogs in Athena:")
        for catalog in catalogs:
            print(
                f"Catalog Name: {catalog['CatalogName']}, "
                f"Type: {catalog['Type']}, "
                f"Description: {catalog.get('Description', 'No description')}"
            )
