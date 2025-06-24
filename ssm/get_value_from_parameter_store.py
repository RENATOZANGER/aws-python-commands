from typing import Any
from config.aws_config import get_session


def get_value_from_parameter_store(client, parameter_name: str, with_decryption: bool = True) -> Any | None:
    """
    Retrieves a value from AWS Systems Manager Parameter Store.
    """
    try:
        response = client.get_parameter(
            Name=parameter_name,
            WithDecryption=with_decryption
        )
        return response['Parameter']['Value']
    except Exception as e:
        print(f"❌ Error retrieving parameter {parameter_name}: {e}")
        return None
    

if __name__ == "__main__":
    ssm_client = get_session().client('ssm')
    parameter_name = '/my/parameter/name'
    
    value = get_value_from_parameter_store(ssm_client, parameter_name)
    
    if value:
        print(f"Value of parameter '{parameter_name}': {value}")
    else:
        print(f"Failed to retrieve value for parameter '{parameter_name}'.")
