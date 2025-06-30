import time
from datetime import datetime, timedelta
from botocore.exceptions import ClientError, BotoCoreError
from config.aws_config import get_session


def get_metrics(cloudwatch, cluster_name, service_name, metric_name, start_time):
    """
    Get cloudwatch metrics for a specific task
    Ecs sends metrics to cloudwatch at 1 minute intervals
    """
    try:
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/ECS',
            MetricName=metric_name,
            Dimensions=[
                {'Name': 'ClusterName', 'Value': cluster_name},
                {'Name': 'ServiceName', 'Value': service_name},
            ],
            StartTime=start_time,
            EndTime=datetime.utcnow(),
            Period=60,
            Statistics=['Maximum']
        )
        if response['Datapoints']:
            return max(datapoint['Maximum'] for datapoint in response['Datapoints'])
        return None
    except Exception as e:
        print(f"❌ Error fetching metric '{metric_name}' for service '{service_name}': {e}")
        return None


def monitor_queues(sqs, queue_urls):
    """
    Monitor SQS queues and print the number of messages in each queue.
    """
    for queue_url in queue_urls:
        try:
            response = sqs.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=['ApproximateNumberOfMessages', 'ApproximateNumberOfMessagesNotVisible']
            )
            num_messages = int(response['Attributes'].get('ApproximateNumberOfMessages', 0))
            num_invisible_messages = int(response['Attributes'].get('ApproximateNumberOfMessagesNotVisible', 0))
            print(f"Queue URL: {queue_url}")
            print(f"Approximate Number of Messages: {num_messages}",
                  f"Approximate Number of Messages in processing: {num_invisible_messages}")
        except (ClientError, BotoCoreError) as e:
            print(f"❌ Error monitoring queue {queue_url}: {e}")
        
def monitor_tasks(ecs, cloudwatch, cluster_name, service_name):
    """
    Monitor ECS tasks for a specific service and collect metrics.
    """
    try:
        tasks_response = ecs.list_tasks(
            cluster=cluster_name,
            serviceName=service_name,
            desiredStatus='RUNNING'
        )
        task_arns = tasks_response.get('taskArns', [])
    
        if not task_arns:
            print(f"No running tasks found for service {service_name} in cluster {cluster_name}.")
            return
    
        total_task_running = 0
    
        if tasks_response['taskArns']:
            describe_response = ecs.describe_tasks(
                cluster=cluster_name,
                tasks=tasks_response['taskArns']
            )
            for task in describe_response['tasks']:
                if task.get('lastStatus') == 'RUNNING':
                    total_task_running += 1
    
        start_time = datetime.utcnow() - timedelta(minutes=3)
        print(f"Tasks with Last Status 'RUNNING': {total_task_running} tasks")
        max_cpu = get_metrics(
            cloudwatch, cluster_name, service_name, 'CPUUtilization', start_time)
        max_memory = get_metrics(
            cloudwatch, cluster_name, service_name, 'MemoryUtilization', start_time)
    
        if max_cpu is not None and max_memory is not None:
            print(f" - Max CPU Utilization: {max_cpu:.2f}% - Max Memory Utilization: {max_memory:.2f}%")
        else:
            print("No metrics data available for CPU or Memory Utilization.")
    
        print(f"Metrics collected: {(start_time - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Execution in: {(datetime.utcnow() - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')}")
    
    except Exception as e:
        print(f"❌ Error monitoring tasks: {e}")

def monitor_sqs_and_tasks(queue_urls, sqs, ecs, cloudwatch, cluster_name, service_name):
    """
    Monitor SQS queues and ECS tasks in a loop, printing metrics every second.
    """
    while True:
        monitor_queues(sqs, queue_urls)
        monitor_tasks(ecs, cloudwatch, cluster_name, service_name)
        print("-" * 50)
        time.sleep(1)
        

if __name__ == "__main__":
    session = get_session()
    sqs = session.client('sqs')
    ecs = session.client('ecs')
    cloudwatch = session.client('cloudwatch')
    queue_urls = [
        'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue',
        'https://sqs.us-east-1.amazonaws.com/123456789012/my-other-queue'
    ]
    cluster_name = 'my-cluster'
    service_name = 'my-service'
    monitor_sqs_and_tasks(queue_urls, sqs, ecs, cloudwatch, cluster_name, service_name)
