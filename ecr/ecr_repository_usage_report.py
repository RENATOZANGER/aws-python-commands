from config.aws_config import get_session


def calculate_ecr_image_storage_and_cost(client, repositories):
    """
    Calculates the storage and cost for ECR images in the provided repositories.
    """
    total_global_size = 0
    total_global_cost = 0

    for repo in repositories:
        try:
            total_size = 0
            image_count = 0
            paginator = client.get_paginator('describe_images')
            page_iterator = paginator.paginate(repositoryName=repo['repositoryName'])
            for page in page_iterator:
                for detail in page.get('imageDetails', []):
                    if 'imageSizeInBytes' in detail:
                        total_size += detail['imageSizeInBytes']
                        image_count += 1
            
            total_size_in_gb = total_size / (1024 ** 3)  # Convert bytes to GB
            monthly_cost = total_size_in_gb * 0.10  # Assuming $0.10 per GB per month
            total_global_size += total_size_in_gb
            total_global_cost += monthly_cost
            
            print(f"Repository: {repo['repositoryName']}")
            print(f"  Total Size: {total_size_in_gb:.2f} GB")
            print(f"  Estimated Monthly Cost: ${monthly_cost:.2f}")
            print(f"Number of Images: {image_count}\n")
            if image_count == 0:
                print(f"  No images found in repository {repo['repositoryName']}.\n")
        
        except Exception as e:
            print(f"❌ Error processing repository {repo['repositoryName']}: {e}")
            continue

    return total_global_size, total_global_cost

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
