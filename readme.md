# Upload blob to azure storage account

This is a simple script to upload a blob to an azure storage account.

It uses sas token to authenticate.

## Usage

```bash
python main.py <path_to_blob> <container_name>
```

>    Note: You need to change the `STORAGE_ACCOUNT_NAME` and `SAS_TOKEN` on your .env file.