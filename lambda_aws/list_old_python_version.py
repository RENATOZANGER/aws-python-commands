from config.aws_config import get_session


def list_old_python_version(lambda_client):
    """
    Lists AWS Lambda functions that are using old Python runtimes.
    """
    response = lambda_client.list_functions()
    old_python_versions = ['python2.7', 'python3.6', 'python3.7', 'python3.8']
    old_functions = []

    for function in response['Functions']:
        if function['Runtime'] in old_python_versions:
            old_functions.append({
                'FunctionName': function['FunctionName'],
                'Runtime': function['Runtime']
            })

    return old_functions

if __name__ == "__main__":
    lambda_client = get_session().client('lambda')
    old_functions = list_old_python_version(lambda_client)
    if old_functions:
        print("Lambda functions with old Python versions:")
        for func in old_functions:
            print(f"Function Name: {func['FunctionName']}, Runtime: {func['Runtime']}")
    else:
        print("No Lambda functions found with old Python versions.")
