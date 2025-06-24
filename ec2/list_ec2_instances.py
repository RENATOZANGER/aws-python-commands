from config.aws_config import get_session


def list_ec2_instances(client):
    """
    Lists the EC2 instances in the AWS account.
    """
    try:
        response = client.describe_instances()
        instances = []
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'State': instance['State']['Name'],
                    'Type': instance['InstanceType'],
                    'LaunchTime': instance['LaunchTime'].isoformat(),
                    'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                    'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                })
        return instances
    except Exception as e:
        print(f"❌ Error listing EC2 instances: {e}")
        return []
    
if __name__ == "__main__":
    ec2_client = get_session().client('ec2')
    instances = list_ec2_instances(ec2_client)
    
    if not instances:
        print("No EC2 instances found or an error occurred.")
    else:
        print("EC2 Instances:")
        for instance in instances:
            print(
                f"Instance ID: {instance['InstanceId']}, "
                f"State: {instance['State']}, "
                f"Type: {instance['Type']}, "
                f"Launch Time: {instance['LaunchTime']},"
                f"Public IP: {instance['PublicIpAddress']}, "
                f"Private IP: {instance['PrivateIpAddress']}"
            )
