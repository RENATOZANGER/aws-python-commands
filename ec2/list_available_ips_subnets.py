from config.aws_config import get_session


def list_available_ips_subnets(client):
    """
    Lists available IPs and subnets in the AWS account.
    """
    try:
        response = client.describe_subnets()
        subnets = []
        for subnet in response.get('Subnets', []):
            subnets.append({
                'SubnetId': subnet['SubnetId'],
                'VpcId': subnet['VpcId'],
                'CidrBlock': subnet['CidrBlock'],
                'AvailableIpAddressCount': subnet['AvailableIpAddressCount'],
                'State': subnet['State'],
            })
        return subnets
    except Exception as e:
        print(f"❌ Error listing available IPs and subnets: {e}")
        return []

if __name__ == "__main__":
    ec2_client = get_session().client('ec2')
    subnets = list_available_ips_subnets(ec2_client)

    if not subnets:
        print("No available IPs or subnets found or an error occurred.")
    else:
        print("Available Subnets:")
        for subnet in subnets:
            print(
                f"Subnet ID: {subnet['SubnetId']}, "
                f"VPC ID: {subnet['VpcId']}, "
                f"CIDR Block: {subnet['CidrBlock']}, "
                f"Available IPs: {subnet['AvailableIpAddressCount']}, "
                f"State: {subnet['State']}"
            )
