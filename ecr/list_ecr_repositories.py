from config.aws_config import get_session


def list_ecr_repositories(client):
    """
    Lists the ECR repositories.
    """
    try:
        response = client.describe_repositories()
        repositories = []
        for repo in response.get('repositories', []):
            repositories.append({
                'RepositoryName': repo['repositoryName'],
                'RepositoryUri': repo['repositoryUri'],
                'CreatedAt': repo['createdAt'].isoformat(),
                'ImageTagMutability': repo['imageTagMutability'],
                'ImageScanningConfiguration': repo.get('imageScanningConfiguration', {}).get('scanOnPush', False),
            })
        return repositories
    except Exception as e:
        print(f"❌ Error listing ECR repositories: {e}")
        return []
    
if __name__ == "__main__":
    ecr_client = get_session().client('ecr')

    repositories = list_ecr_repositories(ecr_client)

    if not repositories:
        print("No ECR repositories found or an error occurred.")
    else:
        print("ECR Repositories:")
        for repo in repositories:
            print(
                f"Repository Name: {repo['RepositoryName']}, "
                f"URI: {repo['RepositoryUri']}, "
                f"Created At: {repo['CreatedAt']}, "
                f"Image Tag Mutability: {repo['ImageTagMutability']}, "
                f"Image Scanning Configuration: {repo['ImageScanningConfiguration']}"
            )
