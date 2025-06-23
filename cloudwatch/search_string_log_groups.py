from botocore.exceptions import ClientError, BotoCoreError
from config.aws_config import get_session
import time
import datetime


def get_all_log_groups(client):
    """
    Gets all CloudWatch log groups.
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

    return log_groups


def search_string_in_log_groups(client, search_string, start_time, end_time):
    """
    Searches for a specific string in all CloudWatch log groups within a specified time range.
    """
    log_groups = get_all_log_groups(client)
    if not log_groups:
        print("❌ No log groups found.")
        return

    for group in log_groups:
        log_group_name = group.get('logGroupName')
        if not log_group_name:
            continue

        print(f"\n🔍 Searching in log group: {log_group_name}")

        next_token = None
        found_in_group = False

        while True:
            try:
                if next_token:
                    response = client.filter_log_events(
                        logGroupName=log_group_name,
                        filterPattern=search_string,
                        startTime=start_time,
                        endTime=end_time,
                        nextToken=next_token
                    )
                else:
                    response = client.filter_log_events(
                        logGroupName=log_group_name,
                        filterPattern=search_string,
                        startTime=start_time,
                        endTime=end_time
                    )

                events = response.get('events', [])

                if events:
                    found_in_group = True
                    for event in events:
                        timestamp = datetime.datetime.fromtimestamp(event['timestamp'] / 1000)
                        message = event.get('message', '')
                        print(f"[{timestamp}] {message}")

                next_token = response.get('nextToken')

                if not next_token:
                    break

            except (ClientError, BotoCoreError) as e:
                print(f"❌ Error searching in {log_group_name}: {e}")
                break

        if not found_in_group:
            print("No matches found.")


if __name__ == "__main__":
    search_string = "ERROR"  # 🔍 String for searching in log groups

    end_time = int(time.time() * 1000)  # Now in milliseconds
    start_time = int((datetime.datetime.now() - datetime.timedelta(days=10)).timestamp() * 1000)  # 10 days ago in milliseconds

    # 🚀 Execute the search
    client = get_session().client('logs')
    search_string_in_log_groups(client, search_string, start_time, end_time)
