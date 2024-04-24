# migrate_aws_ecr_repositories

---

**Python Script for Amazon ECR Repository Replication**

This Python script automates the replication of Amazon Elastic Container Registry (ECR) repositories from a source AWS account to a destination AWS account. The script utilizes the AWS SDK for Python (Boto3) to interact with the Amazon ECR service and perform various actions, including:

1. **Listing ECR Repositories**: The function `get_ecr_repositories()` retrieves a list of ECR repositories from the source AWS account.

2. **Creating ECR Repository**: The function `create_ecr_repository()` creates a new ECR repository in the destination AWS account based on the repositories obtained from the source account. It includes configuration options such as encryption settings and image scanning.

3. **Retrieving Authorization Token**: The function `get_ecr_authorization_token()` retrieves an authorization token for the destination ECR repository. This token is used for authentication when pushing Docker images to the repository.

4. **Tagging and Pushing Images**: The function `tag_and_push_images()` tags and pushes Docker images from the source repository to the corresponding repository in the destination account. It iterates through the images in the source repository, retrieves their manifests, and uploads them to the destination repository.

5. **Main Function**: The `main()` function serves as the entry point of the script. It initializes AWS sessions using AWS profiles, creates ECR clients for both source and destination AWS accounts, retrieves ECR repositories from the source account, and attempts to create corresponding repositories in the destination account.

The script is designed to be configurable by specifying AWS profiles, source and destination repository URIs, and other parameters as needed. It provides a streamlined and automated approach to replicate ECR repositories, facilitating disaster recovery and workload migration scenarios in AWS environments.

## Prerequisites
1. Install AWS cli 2 in the EC2 machine or in local machine.
2. Ensure you have the necessary permissions and configurations for AWS CLI for both source and destination profiles.

###
### 2. `migrate aws ecr`

- **Purpose**: The purpose of this script is to automate the replication of Amazon Elastic Container Registry (ECR) repositories from a source AWS account to a destination AWS account. It is designed to facilitate disaster recovery (DR) scenarios where it's essential to have redundant copies of Docker images stored in ECR repositories across different AWS accounts. By automating this process, the script ensures consistency and reliability in maintaining ECR repositories in both the production (Prod) and DR environments..
- **Usage**: 
  1. **Configure AWS Profiles**: Set up AWS profiles for the source (Prod) and destination (DR) AWS accounts using the AWS CLI.

  2. **Run the Script**: Execute the script using Python 3.x (`python script_name.py`).

  3. **Automated Replication**: The script will automatically:
   - Retrieve ECR repositories from the source AWS account.
   - Create corresponding repositories in the destination AWS account.
   - Tag and push Docker images from source to destination repositories.

  4. **Verification**: Verify successful replication by checking the repositories and images in both accounts using the AWS Management Console or CLI.
