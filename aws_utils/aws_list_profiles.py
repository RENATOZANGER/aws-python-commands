import configparser
import os


def list_aws_profiles() -> list:
    """
    Returns a list of profiles configured in the AWS CLI.
    """
    config_path = os.path.expanduser("~/.aws/config")

    if not os.path.exists(config_path):
        print("File ~/.aws/config not found.")
        return []

    config = configparser.ConfigParser()
    config.read(config_path)

    profiles = []

    for section in config.sections():
        if section.startswith("profile "):
            profile = section.split("profile ")[1]
        else:
            profile = section

        profiles.append(profile)

    if not profiles:
        print("No configured profiles found.")

    return profiles


if __name__ == "__main__":
    profiles = list_aws_profiles()
    print(f"Available profiles:", ", ".join(profiles))
