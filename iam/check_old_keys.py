from datetime import datetime, timezone
from config.aws_config import get_session


def check_old_keys(Limit_Days, iam_client):
    """ Check for old IAM access keys in AWS accounts. """
    users = iam_client.list_users()
    for user in users['Users']:
        username = user['UserName']
        access_keys = iam_client.list_access_keys(UserName=username)

        for chave in access_keys['AccessKeyMetadata']:
            access_key_id = chave['AccessKeyId']
            status = chave['Status']
            creation_date = chave['CreateDate']
            age_in_days = (datetime.now(timezone.utc) - creation_date).days

            # Check if the key is old
            if age_in_days > Limit_Days:
                print(f"\nUser: {username}")
                print(f"  Key: {access_key_id}")
                print(f"  Status: {status}")
                print(f"  Created: {age_in_days} days ({creation_date.date()})")

                # Optional: check last use
                try:
                    last_use = iam_client.get_access_key_last_used(AccessKeyId=access_key_id)
                    data_usage = last_use['AccessKeyLastUsed'].get('LastUsedDate')
                    if data_usage:
                        dias_desde_uso = (datetime.now(timezone.utc) - data_usage).days
                        print(f"  Last used ago: {dias_desde_uso} days ({data_usage.date()})")
                    else:
                        print("  Never been used.")
                except Exception as e:
                    print(f"  Error checking key usage: {e}")

if __name__ == "__main__":
    Limit_Days = 90 # Number of days to consider a key as "old"
    iam_client = get_session().client('iam')
    check_old_keys(Limit_Days, iam_client)
