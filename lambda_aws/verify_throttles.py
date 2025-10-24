from config.aws_config import get_session
from datetime import datetime, timedelta


def verify_throttles(lambda_client, cloudwatch_client):
    """Checks if AWS Lambda functions has throttle in last 24 hours."""
    print("Starting Lambda throttle check for the last 24 hours...")
    try:
        paginator = lambda_client.get_paginator('list_functions')
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        
        for page in paginator.paginate():
            for function in page['Functions']:
                function_name = function['FunctionName']
                
                response = cloudwatch_client.get_metric_statistics(
                    Namespace='AWS/Lambda',
                    MetricName='Throttles',
                    Dimensions=[
                        {
                            'Name': 'FunctionName',
                            'Value': function_name
                        },
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600, # 1 hour (3600 seconds) period for aggregation
                    Statistics=['Sum']
                )
                
                # Sums all data points (throttles) returned in the period
                throttles = sum(datapoint['Sum'] for datapoint in response.get('Datapoints', []))
                if throttles > 0:
                    print(
                        f"⚠️ Lambda function '{function_name}' has been throttled **{int(throttles)}** times in the last 24 hours.")
                else:
                    print(f"✅ Lambda function '{function_name}' has not been throttled in the last 24 hours.")
    
    except Exception as e:
        print(f"❌ Error verifying Lambda functions: {e}")


if __name__ == "__main__":
    try:
        session = get_session()
        lambda_client = session.client('lambda')
        cloudwatch_client = session.client('cloudwatch')
        verify_throttles(lambda_client, cloudwatch_client)
    except Exception as e:
        print(f"❌ Error initializing AWS clients: {e}")
