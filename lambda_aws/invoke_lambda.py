import json
from config.aws_config import get_session



def invoke_lambda(lambda_client, function_name: str, payload: dict) -> dict:
    """
    Invokes an AWS Lambda function with the provided payload.
    """
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse', # Event for asynchronous invocation
            Payload=json.dumps(payload)
        )
        
        if response['StatusCode'] == 200:
            response_payload = json.loads(response['Payload'].read())
            print(f"✅ Successfully invoked '{function_name}': {response_payload}")
            return response_payload
        else:
            print(f"❌ Failed to invoke '{function_name}': {response['FunctionError']}")
            return None
            
    except Exception as e:
        print(f"❌ Error invoking function '{function_name}': {e}")
        return None
    
if __name__ == "__main__":
    lambda_client = get_session().client('lambda')
    
    function_name = 'teste'  # Replace with your Lambda function name
    payload = {
        "key1": "value1",
        "key2": "value2"
    }  # Replace with your desired payload

    invoke_lambda(lambda_client, function_name, payload)
