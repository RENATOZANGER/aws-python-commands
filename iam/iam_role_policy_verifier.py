from config.aws_config import get_session

def check_permissions(statements, action_to_check):
    """
    Checks if the list of statements contains a specific action.
    """
    for statement in statements:
        actions = statement.get('Action', [])
        if isinstance(actions, str):
            actions = [actions]
        for action in actions:
            if action_to_check.lower() == action.lower() or action == '*':
                return True
    return False


def verifier_policies_and_permissions(iam_client, role_name, action_to_check):
    """
    Checks a role's managed and inline policies for permissions related to a specific action.
    """
    try:
        # Check managed policies
        managed_policies = iam_client.list_attached_role_policies(RoleName=role_name)
        print(f"\nManaged Policies attached to role '{role_name}':")
        for policy in managed_policies['AttachedPolicies']:
            print(f" - {policy['PolicyName']} (ARN: {policy['PolicyArn']})")

            # Get the default policy version
            policy_details = iam_client.get_policy(PolicyArn=policy['PolicyArn'])
            policy_version = iam_client.get_policy_version(
                PolicyArn=policy['PolicyArn'],
                VersionId=policy_details['Policy']['DefaultVersionId']
            )
            # Get the policy statements
            statements = policy_version['PolicyVersion']['Document'].get('Statement', [])

            if check_permissions(statements, action_to_check):
                print(f"   -> Policy '{policy['PolicyName']}' CONTAINS permissions for '{action_to_check}'")
            else:
                print(f"   -> Policy '{policy['PolicyName']}' DOES NOT contain permissions for '{action_to_check}'")
            print("---")

        # Check inline policies
        inline_policies = iam_client.list_role_policies(RoleName=role_name)
        print(f"\nInline Policies attached to role '{role_name}':")
        for inline_policy_name in inline_policies['PolicyNames']:
            print(f" - {inline_policy_name}")

            # Get the inline policy document
            inline_policy_document = iam_client.get_role_policy(
                RoleName=role_name,
                PolicyName=inline_policy_name
            )
            statements = inline_policy_document['PolicyDocument'].get('Statement', [])

            if check_permissions(statements, action_to_check):
                print(f"   -> Inline Policy '{inline_policy_name}' CONTAINS permissions for '{action_to_check}'")
            else:
                print(f"   -> Inline Policy '{inline_policy_name}' DOES NOT contain permissions for '{action_to_check}'")
            print("---")

    except Exception as e:
        print(f"Error checking policies for role '{role_name}': {e}")


if __name__ == "__main__":
    role_name = "role_name"
    action_to_check = "s3:GetObject"
    iam_client = get_session().client('iam')
    verifier_policies_and_permissions(iam_client, role_name, action_to_check)
