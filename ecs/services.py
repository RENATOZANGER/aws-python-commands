from botocore.exceptions import ClientError
from config.aws_config import get_session


def list_services(client, cluster_name: str):
    """
    List services in a specific ECS cluster.
    """
    try:
        response = client.list_services(cluster=cluster_name)
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ClusterNotFoundException':
            print(f"❌ Cluster '{cluster_name}' not found.")
            raise
        else:
            print(f"❌ Unexpected error: {e}")
            raise

    services = response.get('serviceArns', [])
    if not services:
        print(f"No services found in cluster {cluster_name}.")
        return

    print(f"Services in the cluster {cluster_name}:")
    for svc in services:
        print(f"- {svc}")

if __name__ == "__main__":
    list_services(get_session().client('ecs'),"cluster_name")
