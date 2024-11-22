import os
import argparse
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

STORAGE_ACCOUNT_NAME = os.getenv("STORAGE_ACCOUNT_NAME")
SAS_TOKEN = os.getenv("SAS_TOKEN")


def upload_folder_to_azure(folder_path, container_name, sas_token):
    # Ensure the folder path is absolute and normalized
    folder_path = os.path.abspath(folder_path)
    root_folder_name = os.path.basename(folder_path)

    # Construct the account URL
    account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net/"

    # Create a BlobServiceClient using the SAS token
    blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)

    # Get the container client
    container_client = blob_service_client.get_container_client(container_name)

    # Walk through the folder
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            # Get the full path of the file
            local_path = os.path.join(root, name)
            # Construct the blob name (include root folder name)
            rel_path = os.path.relpath(local_path, folder_path).replace(os.sep, '/')
            blob_name = f"{root_folder_name}/{rel_path}"

            # Upload the file, preserving folder structure
            with open(local_path, "rb") as data:
                blob_client = container_client.get_blob_client(blob_name)
                blob_client.upload_blob(data, overwrite=True)

    print(f"Folder {folder_path} and its contents have been uploaded to {container_name}.")


if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Upload a folder to Azure Blob Storage.")
    parser.add_argument("folder_path", help="Path to the folder to be uploaded")
    parser.add_argument("container_name", help="Name of the Azure Blob Storage container")
    args = parser.parse_args()

    if args.folder_path and args.container_name:
        upload_folder_to_azure(args.folder_path, args.container_name, SAS_TOKEN)
    else:
        print("Please provide both the folder path and the container name.")
