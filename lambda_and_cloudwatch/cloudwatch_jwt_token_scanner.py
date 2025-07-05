import re
from datetime import datetime, timezone
from botocore.exceptions import ClientError, BotoCoreError
from config.aws_config import get_session
import jwt
import time


def format_timestamp(ms_timestamp):
    dt = datetime.fromtimestamp(ms_timestamp, tz=timezone.utc)
    return dt.strftime('%Y-%m-%d %H:%M:%S UTC')

def extract_token(message, search_string):
    pattern = re.escape(search_string) + r":\s*(\S+)"
    match = re.search(pattern, message)
    return match.group(1) if match else None

def search_string_in_last_log_stream(client, search_string, log_group_name, client_id, time_range_seconds):
    try:
        log_streams = client.describe_log_streams(
            logGroupName=log_group_name,
            orderBy='LastEventTime',
            descending=True,
            limit=10  # Get last 10 log streams
        )
        
        if not log_streams['logStreams']:
            print(f"❌ No log streams found in log group: {log_group_name}")
            return
        
        now = int(time.time() * 1000)
        ten_seconds_ago = now - (time_range_seconds * 1000)
        
        for stream in log_streams['logStreams']:
            events = client.filter_log_events(
                logGroupName=log_group_name,
                logStreamNames=[stream['logStreamName']],
                filterPattern=search_string,
                startTime=ten_seconds_ago,
                endTime=now
            )
            sorted_events = sorted(events['events'], key=lambda x: x['timestamp'], reverse=True)
            for event in sorted_events:
                message = event['message']
                if search_string in message:
                    token_value = extract_token(event['message'], search_string)
                    try:
                        token_decoded = jwt.decode(token_value, options={"verify_signature": False})
                    except jwt.DecodeError:
                        print("❌ Error decoding JWT")
                        continue
                    if token_decoded.get('sub') == client_id:
                        exp_timestamp = token_decoded.get('exp')
                        current_time = datetime.now(timezone.utc).timestamp()
                        if exp_timestamp < current_time:
                            print(f"❌ Token expired in log stream: {stream['logStreamName']}")
                            continue
                        formatted_time = format_timestamp(event['timestamp'] / 1000)
                        formatted_expira = format_timestamp(exp_timestamp)
                        print(f"✅ Found token in log stream: {stream['logStreamName']}")
                        print(f"Bearer {token_value}")
                        print(f"Timestamp: {formatted_time} (UTC-3)")
                        print(f"Expires at: {formatted_expira} (UTC-3)")
                        return
        
        print("❌ No valid tokens found in the last log streams.")
        
    except (ClientError, BotoCoreError) as e:
        print(f"❌ Error searching in log stream: {e}")


if __name__ == "__main__":
    search_string = "Token"  # 🔍 String for searching in log groups
    log_group_name = "/aws/lambda/generate_token"  # 📂 Specify your log group name
    client = get_session().client('logs')
    client_id = "12345"  # Specify your client ID
    time_range_seconds = 120 # search in the last 120 seconds
    search_string_in_last_log_stream(client, search_string, log_group_name, client_id, time_range_seconds)
