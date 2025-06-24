from config.aws_config import get_session


def get_network_interfaces_by_subnet(client):
    """
    Lists network interfaces grouped by subnet.
    """
    try:
        response = client.describe_network_interfaces()
        subnet_groups = {}
        for interface in response.get('NetworkInterfaces', []):
            if interface.get('Groups') and interface['Groups'][0]:
                group_name = interface['Groups'][0].get('GroupName', 'N/A')
            else:
                group_name = 'N/A'
            
            ip_info = {
                'NetworkInterfaceId': interface['NetworkInterfaceId'],
                'SubnetId': interface['SubnetId'],
                'VpcId': interface['VpcId'],
                'PrivateIpAddress': interface.get('PrivateIpAddress', 'N/A'),
                'Status': interface['Status'],
                'GroupName': group_name,
            }
            subnet_id = interface.get('SubnetId', 'N/A')
            if subnet_id not in subnet_groups:
                subnet_groups[subnet_id] = []
            subnet_groups[subnet_id].append(ip_info)
        
        return subnet_groups
    
    except Exception as e:
        print(f"❌ Error listing network interfaces: {e}")
        return []
    
    
if __name__ == "__main__":
    ec2_client = get_session().client('ec2')
    
    network_interfaces = get_network_interfaces_by_subnet(ec2_client)
    
    if not network_interfaces:
        print("No network interfaces found or an error occurred.")
    else:
        print("Network Interfaces by Subnet:")
        for subnet, interfaces in network_interfaces.items():
            print(f"\nSubnet ID: {subnet}")
            for interface in interfaces:
                print(
                    f"Network Interface ID: {interface['NetworkInterfaceId']}, "
                    f"Private IP: {interface['PrivateIpAddress']}, "
                    f"Status: {interface['Status']}, "
                    f"Group Name: {interface['GroupName']}"
                )
