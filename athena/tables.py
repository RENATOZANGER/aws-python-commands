from config.aws_config import get_session
from botocore.exceptions import ClientError


def list_athena_tables(client, catalog='AwsDataCatalog', database='default'):
    """
    Lists the names of the tables in the catalog and database specified in Athena.
    """
    try:
        response = client.list_table_metadata(CatalogName=catalog, DatabaseName=database)
        tables = [table['Name'] for table in response.get('TableMetadataList', [])]
        return tables

    except ClientError as e:
        error_code = e.response['Error'].get('Code', 'Unknown')
        error_message = e.response['Error'].get('Message', str(e))
        print(f"❌ Error listing tables in database '{database}': {error_code} - {error_message}")
        return []

    except Exception as e:
        print(f"❌ Unexpected error while listing tables in database '{database}': {e}")
        return []


if __name__ == "__main__":
    tables = list_athena_tables(get_session().client('athena'))
    if not tables:
        print("No tables found or an error occurred.")
    else:
        print("Tables in Athena:")
        for table in tables:
            print(f"- {table}")
