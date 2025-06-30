import json
from config.aws_config import get_session
from botocore.exceptions import ClientError, BotoCoreError


def start_stepfunctions(client, state_machine_arn, input_dict):
    """
    Starts the execution of a Step Function with the given input.
    """
    try:
        response = client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(input_dict)
        )
        print(f"✅ Execution started successfully: {response['executionArn']}")
        return response
    except (ClientError, BotoCoreError) as e:
        print(f"❌ Error starting execution of Step Function: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    stepfunctions_client = get_session().client('stepfunctions')
    state_machine_arn = "arn:aws:states:us-east-1:123456789012:stateMachine:MyStateMachine"  # Substitua pelo real

    input_dict = {
        "name": "fake",
        "age": "fake"
    }
    start_stepfunctions(stepfunctions_client, state_machine_arn, input_dict)
