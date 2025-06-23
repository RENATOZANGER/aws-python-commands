import boto3
from botocore.exceptions import NoCredentialsError, ProfileNotFound, UnauthorizedSSOTokenError, TokenRetrievalError
from aws_utils.aws_profiles import list_aws_profiles
from aws_utils.sso_login import login

PROFILE_NAME = "user_admin"
REGION_NAME = "us-east-1"

def get_session():
    """
    Gets an AWS session using the configured profile and region.
    If the profile does not exist or the credentials are not valid, displays an appropriate error message.
    If the SSO token is expired, attempts to renew the token.
    If an unexpected error occurs, displays a generic error message.
    """
    
    try:
        session = boto3.Session(profile_name=PROFILE_NAME, region_name=REGION_NAME)
        sts = session.client('sts')
        sts.get_caller_identity()  # Validates if the session is active
        return session

    except ProfileNotFound:
        print(f"❌ Profile '{PROFILE_NAME}' not found. Check the name in the AWS CLI.")
        perfis = list_aws_profiles()
        if perfis:
            print(f"Available profiles:", ", ".join(perfis))
        else:
            print("No profile configured. Run 'aws configure' to configure a new profile.")
        raise
    

    except UnauthorizedSSOTokenError:
        print("❌ SSO token expired. Please run 'aws sso login' to renew.")
        raise

    except NoCredentialsError:
        print("❌ No credentials found. Configure with 'aws configure' or 'aws sso login'.")
        raise
    
    except TokenRetrievalError:
        print("❌ Error retrieving SSO token. Please check your settings.")
        if login("renato_admin"):
            print("🔄 Trying to renew SSO token...")
            return get_session()
        else:
            print("❌ Failed to renew SSO token.")
        raise

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise

# Generic client
def get_client(service_name):
    session = get_session()
    return session.client(service_name)

# Generic resource (for services that support it, like S3, DynamoDB, etc.)
def get_resource(service_name):
    session = get_session()
    return session.resource(service_name)
