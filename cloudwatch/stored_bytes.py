from config.aws_config import get_session


def list_log_groups_sorted_by_stored_bytes(client):
    log_group = []
    next_token = None
    try:
        while True:
            if next_token:
                response = client.describe_log_groups(nextToken=next_token)
            else:
                response = client.describe_log_groups()

            log_group.extend(response.get('logGroups', []))
            next_token = response.get('nextToken')

            if not next_token:
                break

        # Sort log groups by stored bytes in descending order
        sorted_log_groups = sorted(log_group, key=lambda x: x.get('storedBytes', 0), reverse=True)
        max_name_length = 50
        print(f"{'Log Group Name':<{max_name_length}} | {'Stored GB':>15} {'Retention Days':>20}")
        print("-" * (max_name_length + 40))
        
        for group in sorted_log_groups:
            name = group.get('logGroupName', 'N/A')
            stored_bytes = group.get('storedBytes', 0)
            stored_gb = stored_bytes / (1024 ** 3) if stored_bytes else 0
            retention = group.get('retentionInDays', 'N/A')
            
            if len(name) > max_name_length:
                name = name[:max_name_length - 3] + '...'
                
            print(f"{name:<{max_name_length}} | {stored_gb:>15.2f} GB {' ' * 5}{retention:>20} days")

    except Exception as e:
        print(f"❌ Error listing log groups: {e}")
        return []
    

if __name__ == "__main__":
    logs = list_log_groups_sorted_by_stored_bytes(get_session().client('logs'))
