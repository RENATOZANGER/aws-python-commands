import datetime
from config.aws_config import get_session
from collections import Counter

def filter_events_by_name_and_time(client, event_name, start_time, end_time):
    """
    Filters CloudTrail events by event name and time range.
    """
    events = []
    next_token = None
    
    try:
        while True:
            if next_token:
                response = client.lookup_events(
                    LookupAttributes=[{'AttributeKey': 'EventName', 'AttributeValue': event_name}],
                    StartTime=start_time,
                    EndTime=end_time,
                    MaxResults=50,
                    NextToken=next_token
                )
            else:
                response = client.lookup_events(
                    LookupAttributes=[{'AttributeKey': 'EventName', 'AttributeValue': event_name}],
                    StartTime=start_time,
                    EndTime=end_time,
                    MaxResults=50
                )
            
            events.extend(response.get('Events', []))
            next_token = response.get('NextToken')
            if not next_token:
                break
        return events
    except Exception as e:
        print(f"❌ Error fetching CloudTrail events: {e}")
        return []


if __name__ == "__main__":
    client = get_session().client('cloudtrail')
    event_name = 'GetParameter'
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(hours=12)
    print(f"Fetching events for '{event_name}' from {start_time} to {end_time}...\n")
    
    events = filter_events_by_name_and_time(client, event_name, start_time, end_time)
    if events:
        print(f"Found {len(events)} events for '{event_name}':\n")
        usernames = [event['Username'] for event in events if 'Username' in event]
        user_event_count = Counter(usernames)
        print(f"Event counts by user:\n")
        for user, count in user_event_count.items():
            print(f"User: {user}, Event Count: {count}")
    else:
        print(f"No events found for '{event_name}' in the specified time range.")
