from datetime import datetime, timedelta
from config.aws_config import get_session


def execute_query(client, query, log_group_name, start_time, end_time):
    """
    Execute a CloudWatch Logs Insights query.
    """
    response = client.start_query(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        queryString=query,
    )
    
    query_id = response["queryId"]
    
    # Wait for the query to complete
    while True:
        response = client.get_query_results(queryId=query_id)
        if response["status"] == "Complete":
            return response["results"]
        elif response["status"] == "Failed":
            raise Exception("Query failed")
        

if __name__ == "__main__":
    client = get_session().client('logs')

    query = 'fields @timestamp, @message | sort @timestamp desc | limit 20'
    log_group_name = '/aws/lambda/teste'  # Replace with your log group name
    
    start_time = int((datetime.now() - timedelta(days=10)).timestamp() * 1000)  # 10 days ago
    end_time = int(datetime.now().timestamp() * 1000)  # now
    
    # relative_start_time = int(datetime.strptime("2025-06-23T19:40:00Z", "%Y-%m-%dT%H:%M:%SZ").timestamp())
    # relative_end_time = int(datetime.strptime("2025-06-23T23:00:00Z", "%Y-%m-%dT%H:%M:%SZ").timestamp())
    
    query_string = 'fields @timestamp, @message | sort @timestamp desc | limit 20'

    # Execute the query
    results = execute_query(client, query, log_group_name, start_time, end_time)
    
    # Print the results
    for result in results:
        print(result)
