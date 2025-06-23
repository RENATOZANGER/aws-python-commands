import json
import datetime
from collections import defaultdict
from botocore.exceptions import ClientError, BotoCoreError
from config.aws_config import get_session


def get_cloudtrail_events(client, start_time, end_time, event_source, event_name=None):
    """
    Fetches CloudTrail events by filtering by EventSource and optionally EventName.
    """
    events = []

    lookup_attributes = [
        {
            'AttributeKey': 'EventSource',
            'AttributeValue': event_source
        }
    ]

    if event_name:
        lookup_attributes.append({
            'AttributeKey': 'EventName',
            'AttributeValue': event_name
        })

    try:
        response = client.lookup_events(
            LookupAttributes=lookup_attributes,
            StartTime=start_time,
            EndTime=end_time,
            MaxResults=50
        )
        events.extend(response.get('Events', []))

        while 'NextToken' in response:
            response = client.lookup_events(
                LookUpAttributes=lookup_attributes,
                StartTime=start_time,
                EndTime=end_time,
                MaxResults=50,
                NextToken=response['NextToken']
            )
            events.extend(response.get('Events', []))

    except (ClientError, BotoCoreError) as e:
        print(f"❌ Error querying CloudTrail: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    return events


def process_events(events, target_event_name):
    """
    Processes events and counts the occurrence of event_name by role, secret and function.
    """
    event_count = sum(1 for event in events if event['EventName'] == target_event_name)

    role_summary = defaultdict(lambda: {
        'total_events': 0,
        'resources': defaultdict(int),
        'functions': defaultdict(int)
    })

    for event in events:
        try:
            event_data = json.loads(event['CloudTrailEvent'])
            role = event_data.get('userIdentity', {}).get('sessionContext', {}).get('sessionIssuer', {}).get('userName', 'UnknownRole')
            username = event.get('Username', 'UnknownUser')

            if event['EventName'] == target_event_name:
                resource_name = (
                    event.get('Resources', [{}])[0].get('ResourceName', 'UnknownResource')
                    if event.get('Resources')
                    else 'UnknownResource'
                )
                role_summary[role]['total_events'] += 1
                role_summary[role]['resources'][resource_name] += 1
                role_summary[role]['functions'][username] += 1

        except Exception as e:
            print(f"⚠️ Error processing event: {e}")

    return event_count, role_summary


def print_summary(event_count, role_summary, event_name):
    """
    Prints the summary of processed events.
    """
    print(f"\n🔐 Total calls {event_name}: {event_count}")

    for role, data in role_summary.items():
        print(f"\n🔸 Role: {role}")
        print(f"👉 Total of {event_name}: {data['total_events']}")
        print("📜 Resources accessed:")
        for resource, count in data['resources'].items():
            print(f"  - {resource}: {count} times")
        print("👥 Function (users):")
        for function, count in data['functions'].items():
            print(f"  - {function}: {count} times")
        print("-" * 50)


if __name__ == "__main__":
    client = get_session().client('cloudtrail')

    event_source = 'signin.amazonaws.com'
    target_event_name = 'CredentialVerification'

    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=1)

    print(f"⏳ Searching events '{target_event_name}' in Service '{event_source}'...")
    events = get_cloudtrail_events(client, start_time, end_time, event_source, target_event_name)

    if not events:
        print("⚠️ No events found in the period reported.")
    else:
        event_count, role_summary = process_events(events, target_event_name)
        print_summary(event_count, role_summary, target_event_name)
