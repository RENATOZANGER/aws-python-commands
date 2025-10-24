from config.aws_config import get_session


def verify_lambda_with_reserved_concurrency(lambda_client):
    """Checks all Lambda functions for reserved concurrency configuration."""
    try:
        paginator = lambda_client.get_paginator('list_functions')
        for page in paginator.paginate():
            for function in page['Functions']:
                function_name = function['FunctionName']
                
                response = lambda_client.get_function_concurrency(FunctionName=function_name)
                
                reserved_concurrency = response.get('ReservedConcurrentExecutions', -1)
                if reserved_concurrency != -1:
                    print(
                        f"✅ Lambda '{function_name}' has **reserved concurrency** set to **{reserved_concurrency}**.")
                else:
                    print(
                        f"❌ Lambda '{function_name}' **DOES NOT** have reserved concurrency set (using unreserved account concurrency).")
    except Exception as e:
        print(f"❌ Error verifying Lambda functions: {e}")


if __name__ == "__main__":
    try:
        lambda_client = get_session().client('lambda')
        verify_lambda_with_reserved_concurrency(lambda_client)
    except Exception as e:
        print(f"❌ Error initializing Lambda client: {e}")
