import boto3

def get_ecr_repositories(source_ecr_client):
    # Retrieve a list of Amazon ECR repositories in the source account
    response = source_ecr_client.describe_repositories()
    repositories = response.get('repositories', [])
    return repositories

def create_ecr_repository(destination_ecr_client, repository_name):
    # Create a new Amazon ECR repository in the destination account
    response = destination_ecr_client.create_repository(
        repositoryName=repository_name,
         encryptionConfiguration={
        'encryptionType': 'KMS',
        'kmsKey': 'aadc3145-ee7dsd3-42f3-9d42-ca5da9drsdf0f'  # Replace with your KMS key in destination account 
        },
        imageScanningConfiguration={
        'scanOnPush': True
        },
        tags=[
            {
                'Key': 'Name',
                'Value': repository_name
            },
            {
                'Key': 'Environment',
                'Value': 'DR'
            }
        ],
    )

    return response.get('repository', {})

def get_ecr_authorization_token(destination_account_id, destination_region):
    # Retrieve authorization token for the destination Amazon ECR repository
    destination_ecr_client = boto3.client('ecr', region_name=destination_region)
    response = destination_ecr_client.get_authorization_token()

    return response['authorizationData'][0]['authorizationToken'], response['authorizationData'][0]['proxyEndpoint']

def tag_and_push_images(source_repository_uri, destination_repository_uri, source_account_id, destination_account_id, destination_region):
    # Tag and push Docker images from the source repository to the destination repository
    source_ecr_client = boto3.client('ecr')
    destination_ecr_client = boto3.client('ecr', region_name=destination_region)

    source_images = source_ecr_client.list_images(repositoryName=source_repository_uri.split('/')[-1])['imageIds']

    for image in source_images:
        source_image_uri = f"{source_repository_uri}@{image['imageDigest']}"
        destination_image_uri = f"{destination_repository_uri}@{image['imageDigest']}"

        source_image_manifest = source_ecr_client.batch_check_layer_availability(
            repositoryName=source_repository_uri.split('/')[-1],
            layerDigests=[image['imageDigest']]
        )

        if not source_image_manifest['imageManifestResponseList'][0]['imageManifest']:
            print(f"Skipping image {source_image_uri}. Unable to retrieve manifest.")
            continue

        destination_ecr_client.put_image(
            repositoryName=destination_repository_uri.split('/')[-1],
            imageManifest=source_image_manifest['imageManifestResponseList'][0]['imageManifest']
        )

        print(f"Image {source_image_uri} pushed to {destination_image_uri}")

def main():
    # Source account aws cli profile
    source_profile = "sourceprofile"
    # Destination account aws cli profile
    destination_profile = "destinationprofile"

    # Create sessions using AWS profiles
    source_session = boto3.Session(profile_name=source_profile)
    destination_session = boto3.Session(profile_name=destination_profile)

    # Create ECR clients for source and destination sessions
    source_ecr_client = source_session.client("ecr")
    destination_ecr_client = destination_session.client("ecr")
    

    # Step 1: Get ECR repositories in the source account
    source_repositories = get_ecr_repositories(source_ecr_client)
    for repository in source_repositories:
        print(repository['repositoryName'])
        try:
            destination_repository_name = repository['repositoryName']
            # # Step 2: Create a new repository in the destination account with same source repository name
            destination_repository = create_ecr_repository(destination_ecr_client, destination_repository_name)
        except:
            print("Repository already exist...")

if __name__ == "__main__":
    main()
