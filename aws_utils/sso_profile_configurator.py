import os
import boto3
from botocore.exceptions import ProfileNotFound, ClientError, TokenRetrievalError, UnauthorizedSSOTokenError
import subprocess
import configparser

"""
Script for automatic configuration and authentication with AWS SSO (Single Sign-On).

This script performs the following actions:
1. Ensures that the configuration file ~/.aws/config exists.
2. Creates or updates an SSO profile configuration in ~/.aws/config.
3. Attempts to obtain a valid AWS session using the specified profile.
- If the session is expired or missing, automatically logs in via `aws sso login`.
4. After obtaining the session, lists all available S3 buckets in the associated account.
"""

def ensure_aws_config_file_exists():
    """Ensures the ~/.aws/config file and its directory exist."""
    config_dir = os.path.expanduser("~/.aws")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config")
    if not os.path.exists(config_path):
        with open(config_path, 'w'):
            pass


def create_sso_profile_config(
        profile_name: str, sso_account_id: str, sso_role_name: str, sso_start_url: str, sso_region: str
) -> bool:
    """
    Creates or updates an AWS profile and its associated SSO session in the
    AWS CLI configuration file using configparser.
    """
    config_path = os.path.expanduser("~/.aws/config")
    ensure_aws_config_file_exists()
    
    config = configparser.ConfigParser()
    config.optionxform = str
    
    config.read(config_path)
    
    profile_section = f"profile {profile_name}"
    sso_session_section = f"sso-session {profile_name}"
    
    if profile_section not in config:
        config.add_section(profile_section)
        print(f"Adding new profile section: [{profile_section}]")
    else:
        print(f"Updating existing profile section: [{profile_section}]")
    
    config.set(profile_section, "sso_session", profile_name)
    config.set(profile_section, "sso_account_id", sso_account_id)
    config.set(profile_section, "sso_role_name", sso_role_name)
    config.set(profile_section, "region", sso_region)
    
    if sso_session_section not in config:
        config.add_section(sso_session_section)
        print(f"Adding new SSO session section: [{sso_session_section}]")
    else:
        print(f"Updating existing SSO session section: [{sso_session_section}]")
    
    config.set(sso_session_section, "sso_start_url", sso_start_url)
    config.set(sso_session_section, "sso_region", sso_region)
    config.set(sso_session_section, "sso_registration_scopes", "sso:account:access")
    
    try:
        with open(config_path, 'w') as config_file:
            config.write(config_file)
        print(f"AWS config file updated for profile '{profile_name}'.")
        return True
    except Exception as e:
        print(f"Error writing to config file: {e}")
        return False


def try_sso_login_and_get_session(profile_name: str, region: str) -> boto3.Session | None:
    """Helper function to perform SSO login and then return a session."""
    try:
        print(f"Initiating AWS SSO login for profile '{profile_name}'...")
        subprocess.run(
            ["aws", "sso", "login", "--profile", profile_name],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ AWS SSO login command completed for profile '{profile_name}'.")
        new_session = boto3.Session(profile_name=profile_name, region_name=region)
        
        # Verify the new session immediately
        new_session.client('sts').get_caller_identity()
        print(f"✅ Successfully obtained and validated new SSO session for profile '{profile_name}'.")
        return new_session
    except subprocess.CalledProcessError as sub_e:
        print(f"🚨 Error during AWS SSO login for profile '{profile_name}': {sub_e.stderr}")
        return None
    except ClientError as ce:  # Catch ClientError if get_caller_identity fails right after login
        print(f"🚨 New session validation failed after SSO login for profile '{profile_name}': {ce}")
        return None
    except Exception as login_e:
        print(f"🚨 An unexpected error occurred during SSO login or session validation: {login_e}")
        return None


def get_aws_session_with_sso(profile_name: str, region: str) -> boto3.Session | None:
    """
    Attempts to get an AWS session for a given SSO profile.
    If the SSO token is expired, not present, or refresh failed, it initiates an SSO login.
    """
    try:
        session = boto3.Session(profile_name=profile_name)
        sts_client = session.client('sts')
        sts_client.get_caller_identity()
        print(f"✅ Existing SSO session for profile '{profile_name}' is valid.")
        return session
    except ProfileNotFound:
        print(f"❌ Profile '{profile_name}' not found in ~/.aws/config. Please ensure it's configured.")
        return None
    except (TokenRetrievalError, ClientError) as e:  # Catch both here, simplified
        print(
            f"❌ SSO token for profile '{profile_name}' expired, invalid, or refresh failed: {e}. Attempting to log in...")
        return try_sso_login_and_get_session(profile_name, region)
    except UnauthorizedSSOTokenError as e:
        print(f"❌ Unauthorized SSO token for profile '{profile_name}': {e}. Attempting to log in...")
        return try_sso_login_and_get_session(profile_name, region)
    except Exception as e:
        print(f"🚨 An unexpected error occurred while trying to get session: {e}")
        return None


def list_s3_buckets(session: boto3.Session) -> list[str]:
    """Lists S3 buckets using the provided boto3 session."""
    try:
        s3 = session.client('s3')
        response = s3.list_buckets()
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]
        print(f"Found {len(bucket_names)} S3 buckets.")
        return bucket_names
    except ClientError as e:
        print(f"🚨 Error listing S3 buckets: {e}")
        return []
    except Exception as e:
        print(f"🚨 An unexpected error occurred while listing buckets: {e}")
        return []


if __name__ == "__main__":
    target_profile_name = 'profile_name'
    
    sso_start_url_example = 'https://xxxxxxxxx.awsapps.com/start'
    region = 'us-east-1'
    
    print(f"Attempting to configure/update profile '{target_profile_name}' in ~/.aws/config...")
    config_success = create_sso_profile_config(
        profile_name=target_profile_name,
        sso_account_id='xxxxxxxxxx',  # Replace with your AWS Account ID
        sso_role_name='AdministratorAccess',
        sso_start_url=sso_start_url_example,
        sso_region=region
    )
    
    if not config_success:
        print("🛑 Failed to configure AWS profile. Exiting.")
        exit(1)
    
    print(f"\nAttempting to get AWS session for profile '{target_profile_name}'...")
    aws_session = get_aws_session_with_sso(target_profile_name, region)
    
    if aws_session:
        print("\nListing S3 buckets...")
        buckets = list_s3_buckets(aws_session)
        if buckets:
            print("Available S3 buckets:")
            for bucket in buckets:
                print(f"- {bucket}")
        else:
            print("No S3 buckets found or an error occurred.")
    else:
        print("🛑 Could not obtain a valid AWS session. Cannot list buckets.")
