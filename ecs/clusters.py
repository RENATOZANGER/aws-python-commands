from config.aws_config import get_session
from botocore.exceptions import ClientError


def clusters_list(client):
    """List ECS clusters"""
    try:
        response = client.list_clusters()
        clusters = response.get('clusterArns', [])
        
        if not clusters:
            print("No clusters found.")
            return
        
        print("ECS clusters found:")
        for cluster in clusters:
            print(f"- {cluster}")
    
    except ClientError as e:
        error_code = e.response['Error'].get('Code', 'Unknown')
        error_message = e.response['Error'].get('Message', str(e))
        print(f"❌ Error listing clusters: {error_code} - {error_message}")
    
    except Exception as e:
        print(f"❌ Unexpected error while listing clusters: {e}")


if __name__ == "__main__":
    client = get_session().client('ecs')
    clusters_list(client)
