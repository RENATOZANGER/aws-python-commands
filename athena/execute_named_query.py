import time
from config.aws_config import get_session
from botocore.exceptions import ClientError

def execute_named_query(client):
    """
    Executes a Named Query on AWS Athena and displays the results.
    """
    try:
        batch_get_named_querys = client.batch_get_named_query(
            NamedQueryIds=['b14c4f8b-0d1e-4c3a-9f2b-5e6d7e8f9a0b']  # Replace with your Named Query ID
        )
        named_query = batch_get_named_querys['NamedQueries'][0]
        query_string = named_query['QueryString']
    except ClientError as e:
        print(f"❌ Error getting Named Query: {e.response['Error'].get('Message', str(e))}")
        return
    except Exception as e:
        print(f"❌ Unexpected error while getting Named Query: {e}")
        return

    try:
        response_query = client.start_query_execution(
            QueryString=query_string,
            QueryExecutionContext={'Database': 'default'},
            ResultConfiguration={'OutputLocation': 's3://bucket-output/query-results/'}
        )
    except ClientError as e:
        print(f"❌ Error starting query execution: {e.response['Error'].get('Message', str(e))}")
        return
    except Exception as e:
        print(f"❌ Unexpected error when starting query execution: {e}")
        return

    try:
        while True:
            response = client.get_query_execution(QueryExecutionId=response_query['QueryExecutionId'])
            status = response['QueryExecution']['Status']['State']

            if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                print(f"Query execution finished with status: {status}")
                time.sleep(1)
                break
            else:
                print("Query is still running...")
                time.sleep(1)
    except ClientError as e:
        print(f"❌ Error when checking execution status: {e.response['Error'].get('Message', str(e))}")
        return
    except Exception as e:
        print(f"❌ Unexpected error while querying execution status: {e}")
        return

    if status == 'SUCCEEDED':
        try:
            results = client.get_query_results(QueryExecutionId=response_query['QueryExecutionId'])

            keys = [data['VarCharValue'] for data in results['ResultSet']['Rows'][0]['Data']]

            for row in results['ResultSet']['Rows'][1:]:
                values = [data.get('VarCharValue', '') for data in row['Data']]
                for key, value in zip(keys, values):
                    print(f"{key}: {value}")
        except ClientError as e:
            print(f"❌ Error getting query results: {e.response['Error'].get('Message', str(e))}")
        except Exception as e:
            print(f"❌ Unexpected error while retrieving query results: {e}")
    else:
        print(f"Query failed with status: {status}")


if __name__ == "__main__":
    execute_named_query(get_session().client('athena'))
