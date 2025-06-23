from config.aws_config import get_session
from botocore.exceptions import ClientError


def list_athena_named_queries(client):
    """
    Lists the IDs of Named Queries in Athena.
    """
    try:
        response = client.list_named_queries()
        return response.get('NamedQueryIds', [])
    except ClientError as e:
        error_code = e.response['Error'].get('Code', 'Unknown')
        error_message = e.response['Error'].get('Message', str(e))
        print(f"❌ Error listing Named Queries: {error_code} - {error_message}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error while listing Named Queries: {e}")
        return []


def get_athena_named_query(client, query_id):
    """
    Returns the details of a specific Named Query.
    """
    try:
        response = client.get_named_query(NamedQueryId=query_id)
        return response.get('NamedQuery', {})
    except ClientError as e:
        error_code = e.response['Error'].get('Code', 'Unknown')
        error_message = e.response['Error'].get('Message', str(e))
        print(f"❌ Error getting details of Query ID {query_id}: {error_code} - {error_message}")
        return {}
    except Exception as e:
        print(f"❌ Unexpected error while getting Query ID details {query_id}: {e}")
        return {}


if __name__ == "__main__":
    client = get_session().client('athena')
    named_queries = list_athena_named_queries(client)

    if not named_queries:
        print("No Named Query found or an error occurred.")
    else:
        print("Named Queries in Athena:")
        for query_id in named_queries:
            query = get_athena_named_query(client, query_id)
            if query:
                print(
                    f"Query ID: {query.get('NamedQueryId')}, "
                    f"Name: {query.get('Name')}, "
                    f"Description: {query.get('Description', 'No description')}"
                )
            else:
                print(f"⚠️ Unable to get details for Query ID {query_id}")
