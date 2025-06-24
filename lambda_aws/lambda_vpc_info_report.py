from config.aws_config import get_session


def list_lambda_functions_with_vpc_info(lambda_client):
    """
    Lists AWS Lambda functions and their VPC configuration.
    """
    functions = []
    next_marker = None
    
    while True:
        if next_marker:
            response = lambda_client.list_functions(Marker=next_marker)
        else:
            response = lambda_client.list_functions()
        
        functions.extend(response['Functions'])
        if 'NextMarker' in response:
            next_marker = response['NextMarker']
        else:
            break

    return functions

def filter_vpc_functions(lambda_client, functions):
    """
    Filters and prints AWS Lambda functions that are configured with VPC.
    """
    for function in functions:
        function_name = function['FunctionName']
        print(f"Checking VPC configuration for function: {function_name}")
        function_config = lambda_client.get_function_configuration(FunctionName=function_name)
        
        if 'VpcConfig' in function_config and 'SubnetIds' in function_config['VpcConfig']:
            subnet_ids = function_config['VpcConfig']['SubnetIds']
            print(f"Subnet IDs: {', '.join(subnet_ids)}")
        else:
            print(f"Function '{function_name}' is not configured with VPC.")
    
        print("" + "-" * 40)
    
if __name__ == "__main__":
    lambda_client = get_session().client('lambda')

    functions = list_lambda_functions_with_vpc_info(lambda_client)
    filter_vpc_functions(lambda_client, functions)
