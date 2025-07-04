import configparser
import os


def create_profile(
        profile_name: str,
        sso_account_id: str,
        sso_role_name: str,
        sso_start_url: str,
        sso_region: str
) -> list:
    """
    Creates a new AWS profile and its associated SSO session in the AWS CLI configuration file.
    """
    config_path = os.path.expanduser("~/.aws/config")
    
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    config = configparser.ConfigParser()
    
    config.optionxform = str
    
    if os.path.exists(config_path):
        config.read(config_path)
    
    profile_section = f"profile {profile_name}"
    sso_session_section = f"sso-session {profile_name}"
    
    if profile_section in config or sso_session_section in config:
        print(f"Profile or SSO session '{profile_name}' already exists. Skipping creation.")
        return []
    
    # Add the profile section
    config.add_section(profile_section)
    config.set(profile_section, "sso_session", profile_name)
    config.set(profile_section, "sso_account_id", sso_account_id)
    config.set(profile_section, "sso_role_name", sso_role_name)
    config.set(profile_section, "region", sso_region)  # É comum definir a região padrão aqui também
    
    # Add SSO session section
    config.add_section(sso_session_section)
    config.set(sso_session_section, "sso_start_url", sso_start_url)
    config.set(sso_session_section, "sso_region", sso_region)
    config.set(sso_session_section, "sso_registration_scopes", "sso:account:access")
    
    try:
        with open(config_path, 'w') as config_file:
            config.write(config_file)
        print(f"Profile '{profile_name}' and SSO session created successfully.")
        return [profile_name]
    except Exception as e:
        print(f"Error writing to config file: {e}")
        return []


if __name__ == "__main__":
    profile_name = 'profile_name'
    sso_account_id = 'account_id'
    sso_role_name = 'AdministratorAccess'
    sso_start_url = 'https://d-xxxxxxxxxx.awsapps.com/start'
    sso_region = 'us-east-1'
    
    profiles = create_profile(
        profile_name=profile_name,
        sso_account_id=sso_account_id,
        sso_role_name=sso_role_name,
        sso_start_url=sso_start_url,
        sso_region=sso_region
    )
    if profiles:
        print(f"Available profiles:", ", ".join(profiles))
    else:
        print("No profiles were created or they already existed.")
