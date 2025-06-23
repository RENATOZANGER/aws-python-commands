from config.aws_config import get_session
from botocore.exceptions import ClientError


def List_tasks(client, cluster_name: str, service_name: str):
    """List the tasks of an ECS service"""
    try:
        response = client.list_tasks(
            cluster=cluster_name,
            serviceName=service_name
        )
        task_arns = response.get('taskArns', [])

        if not task_arns:
            print(f"No tasks found in the service {service_name} in cluster {cluster_name}.")
            return

        print(f"Tasks in the service {service_name}:")
        for task in task_arns:
            print(f"- {task}")

    except ClientError as e:
        error_code = e.response['Error'].get('Code', 'Unknown')
        error_message = e.response['Error'].get('Message', str(e))
        print(f"❌ Error listing tasks: {error_code} - {error_message}")

    except Exception as e:
        print(f"❌ Unexpected error while listing tasks: {e}")


if __name__ == "__main__":
    cluster_name = "your_cluster_name"  # 🔧 Replace with actual cluster name
    service_name = "your_service_name"  # 🔧 Replace with actual service name
    List_tasks(get_session().client('ecs'), cluster_name, service_name)
