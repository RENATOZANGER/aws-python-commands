from config.aws_config import get_session
from botocore.exceptions import ClientError

def list_athena_workgroups(client):
    """
    Lists the Athena workgroups in the AWS account.
    """
    try:
        response = client.list_work_groups()
        return response.get('WorkGroups', [])
    except ClientError as e:
        error_code = e.response['Error'].get('Code', 'Unknown')
        error_message = e.response['Error'].get('Message', str(e))
        print(f"❌ Error listing Athena workgroups: {error_code} - {error_message}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error when listing Athena workgroups: {e}")
        return []

if __name__ == "__main__":
    workgroups = list_athena_workgroups(get_session().client('athena'))
    if not workgroups:
        print("No Athena workgroups found.")
    else:
        print("Athena Workgroups:")
        for wg in workgroups:
            print(f"- Name: {wg['Name']}, State: {wg['State']}, Description: {wg.get('Description', 'No description')}")
