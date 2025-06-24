from config.aws_config import get_session


def get_latest_lambda_version_details(lambda_client, function_name: str) -> dict | None:
    """
    Retrieves the latest version details of a specified AWS Lambda function.
    """
    try:
        response = lambda_client.list_versions_by_function(FunctionName=function_name)
        versions = response.get('Versions', [])
        latest_version = versions[-1] if versions else None
        if latest_version:
            print(f"✅ Latest version: '{latest_version['Version']}':")
            print(f"Function Name: {latest_version['FunctionName']}")
            print(f"Description: {latest_version.get('Description', 'No description')}")
            print(f"Last Modified: {latest_version['LastModified']}")
            print(f"Memory Size: {latest_version['MemorySize']} MB")
            print(f"Ephemeral Storage Size: {latest_version['EphemeralStorage']['Size']} MB")
            print(f"Timeout: {latest_version['Timeout']} seconds")
            print(f"Runtime: {latest_version['Runtime']}")
            print(f"Handler: {latest_version['Handler']}")
            print(f"Role: {latest_version['Role']}")
            print(f"Architecture: {latest_version['Architectures']}")
            code_size_mb = latest_version['CodeSize'] / (1024 * 1024)
            print(f"Code Size: {code_size_mb:.2f} MB")
        else:
            print(f"❌ No versions found for function '{function_name}'.")
            return None
    
    except Exception as e:
        print(f"❌ Error retrieving versions for function '{function_name}': {e}")
        return None

if __name__ == "__main__":
    lambda_client = get_session().client('lambda')

    function_name = 'lambda_function_name'  # Replace with your Lambda function name

    version_details = get_latest_lambda_version_details(lambda_client, function_name)
