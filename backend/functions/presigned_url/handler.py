import os
import json
import uuid
import boto3

from response import success, error

s3_client   = boto3.client("s3")
BUCKET_NAME = os.environ["S3_BUCKET"]

def lambda_handler(event, context):
    claims = event.get("requestContext", {}) \
                  .get("authorizer", {}) \
                  .get("jwt", {}) \
                  .get("claims", {})
    user_id = claims.get("sub")

    # Local development fallback
    if not user_id and os.environ.get("AWS_SAM_LOCAL") == "true":
        user_id = "local-test-user"

    if not user_id:
        return error("Unauthorized", 401)

    body          = __import__("json").loads(event.get("body") or "{}")
    filename      = body.get("filename", "")
    content_type  = body.get("contentType", "application/octet-stream")

    if not filename:
        return error("filename is required")

    key = f"uploads/{user_id}/{uuid.uuid4()}/{filename}"

    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket":      BUCKET_NAME,
            "Key":         key,
            "ContentType": content_type
        },
        ExpiresIn=300  # 5 minutes
    )

    return success({
        "uploadUrl": presigned_url,
        "fileKey":   key
    })