# Alfred Workflow: Upload Screenshot to Cloudflare R2 Storage

This workflow helps you upload a screenshot from your clipboard or local disk to Cloudflare R2 and puts the public URL of the image to your clipboard.

## Overview

This workflow is written in Python. It uses Boto3 as the AWS client to upload images.

## Demo


https://github.com/PatelUtkarsh/Alfred-Workflow-Upload-R2/assets/5015489/1559487b-f51b-45b4-9785-e92f315df870



## Download

https://github.com/PatelUtkarsh/Alfred-Workflow-Upload-R2/releases

## Usage

Check https://www.cloudflare.com/developer-platform/r2/ on how to get environment variables.

Config Environment Variables:

- cf_access_key: Cloudflare access key
- cf_account_id: Cloudflare access secret
- cf_secret_key: Cloudflare access secret
- cf_bucket_name: Cloudflare bucket name. e.g. `my-bucket-name`
- cf_region: Cloudflare region (Must be one of: wnam, enam, weur, eeur, apac, auto).
- tinypng_api_key: Get your tinypng API key from https://tinypng.com/developers to compress images before uploading.
- shorturl: If you have proxy to bucket via CloudFlare use that url.

Upload image from clipboard:

```bash
upload
```

Upload image from local:

```bash
upload TYPE-FILENAME-HERE
```

Upload clipboard text file:
```bash
pb
```

## Forked source: 🙌
- https://github.com/tonyxu-io/Alfred-Workflow-Upload-S3
