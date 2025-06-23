import json
import os
import glob


def list_active_profiles():
    """
    Lists SSO profiles with active tokens.
    """
    folder_path = os.path.expanduser("~/.aws/sso/cache/*.json")
    json_files = glob.glob(folder_path)

    if not json_files:
        print("No active SSO tokens found.")
        return

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                start_url = data.get('startUrl', 'Unknown')
                expires_at = data.get('expiresAt', 'Unknown')

                print(f"\n🌐 Start URL: {start_url}")
                print(f"⏳ Expires on: {expires_at}")

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

if __name__ == "__main__":
    list_active_profiles()
