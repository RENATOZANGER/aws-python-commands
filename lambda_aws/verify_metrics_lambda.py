from config.aws_config import get_session
from datetime import datetime, timedelta, timezone


def verify_lambda_metrics(lambda_client, cloudwatch_client, metric_name):
    """Checks the specified AWS Lambda metric (given by `metric_name`) for all functions within the last 24 hours."""
    print(f"Starting Lambda metric verification for '{metric_name}' in the last 24 hours...\n")
    try:
        paginator = lambda_client.get_paginator('list_functions')

        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=24)

        for page in paginator.paginate():
            for function in page['Functions']:
                function_name = function['FunctionName']

                response = cloudwatch_client.get_metric_statistics(
                    Namespace='AWS/Lambda',
                    MetricName=metric_name,
                    Dimensions=[
                        {
                            'Name': 'FunctionName',
                            'Value': function_name
                        },
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,  # 1-hour aggregation
                    Statistics=['Sum']
                )

                metric_sum = sum(dp['Sum'] for dp in response.get('Datapoints', []))

                if metric_sum > 0:
                    print(f"⚠️  Lambda function '{function_name}' — {metric_name}: {int(metric_sum)} in the last 24 hours.")
                else:
                    print(f"✅  Lambda function '{function_name}' — no {metric_name.lower()} in the last 24 hours.")

    except Exception as e:
        print(f"❌ Error verifying Lambda metrics: {e}")


if __name__ == "__main__":
    try:
        session = get_session()
        lambda_client = session.client('lambda')
        cloudwatch_client = session.client('cloudwatch')
        metric_name = 'Throttles'  # Example: 'Invocations', 'Errors', 'Duration'
        verify_lambda_metrics(lambda_client, cloudwatch_client, metric_name)
    except Exception as e:
        print(f"❌ Error initializing AWS clients: {e}")
