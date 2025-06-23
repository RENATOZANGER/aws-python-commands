import subprocess

def login(profile: str):
    """
    Executes 'aws sso login' for the given profile.
    """
    try:
        print(f"🔐 Logging into profile '{profile}'...")
        result = subprocess.run(
            ["aws", "sso", "login", "--profile", profile],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ SSO login successful!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing SSO login:\n{e.stderr}")
        return False

if __name__ == "__main__":
    login("user_admin")
