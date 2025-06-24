from config.aws_config import get_session


def list_all_services(client, cluster_name):
    """
    Lists all ECS services in the specified cluster.
    """
    try:
        paginator = client.get_paginator('list_services')
        response_iterator = paginator.paginate(cluster=cluster_name)
        services = []
        for page in response_iterator:
            services.extend(page.get('serviceArns', []))
        return services

    except Exception as e:
        print(f"❌ Error listing services in cluster {cluster_name}: {e}")
        return []
    
def get_fargate_version(client, cluster_name, service_name):
    """
    Retrieves the Fargate version for a specific ECS service.
    """
    try:
        response = client.describe_services(
            cluster=cluster_name,
            services=[service_name]
        )
        if 'services' in response and len(response['services']) > 0:
            service = response['services'][0]
            if 'PlatformVersion' in service:
                return service['PlatformVersion']
            else:
                return 'LATEST'
        
        return None
    
    except Exception as e:
        print(f"❌ Error retrieving Fargate version for service {service_name}: {e}")
        return 'Error retrieving Fargate version.'
    
if __name__ == "__main__":
    ecs_client = get_session().client('ecs')

    cluster_name = 'your-cluster-name'

    services = list_all_services(ecs_client, cluster_name)

    if not services:
        print("No services found in the specified cluster.")
    else:
        for service_arn in services:
            service_name = service_arn.split('/')[-1]  # Extract service name from ARN
            fargate_version = get_fargate_version(ecs_client, cluster_name, service_name)
            print(f"Service: {service_name}, Fargate Version: {fargate_version}")
