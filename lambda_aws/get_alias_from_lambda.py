from config.aws_config import get_session


def get_alias_from_all_lambdas(lambda_client):
    """
    Retrieves aliases for all AWS Lambda functions.
    """
    all_functions = []
    paginator = lambda_client.get_paginator('list_functions')
    for page in paginator.paginate():
        all_functions.extend(page['Functions'])
        
    for function in all_functions:
        function_name = function['FunctionName']
        aliases = lambda_client.list_aliases(FunctionName=function_name).get('Aliases', [])
        
        if len(aliases) > 1:
            print(f"Function: {function_name} has multiple aliases:")
            for alias in aliases:
                print(f"  Alias Name: {alias['Name']}, Alias ARN: {alias['AliasArn']}")
        elif len(aliases) == 1:
            alias = aliases[0]
            print(f"Function: {function_name} has a single alias:")
            print(f"  Alias Name: {alias['Name']}, Alias ARN: {alias['AliasArn']}")
        else:
            print(f"Function: {function_name} has no aliases.")


if __name__ == "__main__":
    lambda_client = get_session().client('lambda')
    
    aliases = get_alias_from_all_lambdas(lambda_client)
