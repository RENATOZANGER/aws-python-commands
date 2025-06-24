from config.aws_config import get_session


def calculate_ecr_image_storage_and_cost(client, repositories):
    """
    Calculates the storage and cost for ECR images in the provided repositories.
    """
    total_storage = 0
    total_cost = 0.0
    storage_cost_per_gb = 0.10  # Example cost per GB of storage

    for repo in repositories:
        try:
            response = client.describe_images(repositoryName=repo['RepositoryName'])
            images = response.get('imageDetails', [])
            for image in images:
                if 'imageSizeInBytes' in image:
                    size_gb = image['imageSizeInBytes'] / (1024 ** 3)  # Convert bytes to GB
                    total_storage += size_gb
                    total_cost += size_gb * storage_cost_per_gb
        except Exception as e:
            print(f"❌ Error calculating storage for repository {repo['RepositoryName']}: {e}")

    return total_storage, total_cost

def generate_ecr_repository_usage_report(client):
    """
    Generates a report of ECR repository usage including storage and cost.
    """
    try:
        response = client.describe_repositories()
        repositories = response.get('repositories', [])
        
        if not repositories:
            print("No ECR repositories found.")
            return

        total_storage, total_cost = calculate_ecr_image_storage_and_cost(client, repositories)

        print("ECR Repository Usage Report:")
        print(f"Total Storage Used: {total_storage:.2f} GB")
        print(f"Estimated Total Cost: ${total_cost:.2f}")

    except Exception as e:
        print(f"❌ Error generating ECR repository usage report: {e}")
        

if __name__ == "__main__":
    ecr_client = get_session().client('ecr')
    generate_ecr_repository_usage_report(ecr_client)
