from botocore.exceptions import ClientError, BotoCoreError
from config.aws_config import get_session


def get_all_log_groups(client):
    """
    Fetches all CloudWatch log groups.
    """
    log_groups = []
    next_token = None
    while True:
        try:
            if next_token:
                response = client.describe_log_groups(nextToken=next_token)
            else:
                response = client.describe_log_groups()

            log_groups.extend(response.get('logGroups', []))
            next_token = response.get('nextToken')

            if not next_token:
                break

        except (ClientError, BotoCoreError) as e:
            print(f"❌ Error fetching log groups: {e}")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            break
    
    return log_groups

def print_log_groups(client, log_groups):
    """
    Check if the log group has log streams and print the log group name.
    """
    if not log_groups:
        print("No log groups found.")
        return

    for group in log_groups:
        log_group_name = group.get('logGroupName', 'N/A')
        log_streams = client.describe_log_streams(logGroupName=log_group_name).get('logStreams', [])
        
        if not log_streams:
            print(f"No log streams found for log group: {log_group_name}")
            continue
        
if __name__ == "__main__":
    client = get_session().client('logs')
    log_groups = get_all_log_groups(client)
    print_log_groups(client, log_groups)
