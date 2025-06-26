from config.aws_config import get_session


def get_alias__version_from_all_lambdas(lambda_client):
    """
    List all AWS Lambda functions, their aliases, and the last numbered version for each function.
    """
    all_functions = []
    paginator = lambda_client.get_paginator('list_functions')
    for page in paginator.paginate():
        all_functions.extend(page['Functions'])
        
    for function in all_functions:
        function_name = function['FunctionName']
        aliases = lambda_client.list_aliases(FunctionName=function_name).get('Aliases', [])
        
        versions = lambda_client.list_versions_by_function(FunctionName=function_name).get('Versions', [])
        
        numbered_versions = [version for version in versions if version['Version'] != '$LATEST']
        
        last_numbered_version = numbered_versions[-1]['Version'] if numbered_versions else 'N/A'

        if aliases:
            print(f"Function: {function_name}")
            print(f" - Last Numbered Version: {last_numbered_version}")
            for alias in aliases:
                print(f" - Alias: {alias['Name']}, Version: {alias['FunctionVersion']}")
        else:
            print(f"Function: {function_name}")
            print(f" - Last Numbered Version: {last_numbered_version}")
            print(" - Alias: No Aliases found")
        print("" + "-" * 40)
        
        
if __name__ == "__main__":
    lambda_client = get_session().client('lambda')
    
    aliases = get_alias__version_from_all_lambdas(lambda_client)
