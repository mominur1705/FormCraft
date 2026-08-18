import json
import uuid
import os
from datetime import datetime, timezone

from db import get_table
from response import success, error

def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    path   = event.get("rawPath", "")

    if method == "POST" and path == "/forms":
        return create_form(event)
    elif method == "GET" and "/forms/" in path and "/responses" not in path:
        return get_form(event)
    elif method == "GET" and path == "/forms":
        return list_forms(event)
    elif method == "DELETE" and "/forms/" in path:
        return delete_form(event)
    else:
        return error("Route not found", 404)


def _get_user_id(event):
    """Extract userId from Cognito JWT claims.
    Falls back to a local test user when running via SAM."""
    claims = event.get("requestContext", {}) \
                  .get("authorizer", {}) \
                  .get("jwt", {}) \
                  .get("claims", {})
    user_id = claims.get("sub")

    # Local development fallback
    if not user_id and os.environ.get("AWS_SAM_LOCAL") == "true":
        user_id = "local-test-user"

    return user_id


def create_form(event):
    user_id = _get_user_id(event)
    if not user_id:
        return error("Unauthorized", 401)

    body = json.loads(event.get("body") or "{}")
    title  = body.get("title", "").strip()
    fields = body.get("fields", [])

    if not title:
        return error("title is required")

    form_id  = str(uuid.uuid4())
    now      = datetime.now(timezone.utc).isoformat()

    table = get_table()

    # Main item: queryable by user
    table.put_item(Item={
        "PK":        f"USER#{user_id}",
        "SK":        f"FORM#{form_id}",
        "GSI1PK":   f"FORM#{form_id}",
        "GSI1SK":   "METADATA",
        "formId":    form_id,
        "userId":    user_id,
        "title":     title,
        "fields":    fields,
        "status":    "active",
        "createdAt": now,
        "updatedAt": now,
    })

    return success({"formId": form_id, "title": title}, 201)


def get_form(event):
    path_params = event.get("pathParameters") or {}
    form_id     = path_params.get("formId")
    if not form_id:
        return error("formId is required")

    table = get_table()

    result = table.query(
        IndexName="GSI1",
        KeyConditionExpression="GSI1PK = :pk AND GSI1SK = :sk",
        ExpressionAttributeValues={
            ":pk": f"FORM#{form_id}",
            ":sk": "METADATA"
        }
    )

    items = result.get("Items", [])
    if not items:
        return error("Form not found", 404)

    return success(items[0])


def list_forms(event):
    user_id = _get_user_id(event)
    if not user_id:
        return error("Unauthorized", 401)

    table = get_table()

    result = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :prefix)",
        ExpressionAttributeValues={
            ":pk":     f"USER#{user_id}",
            ":prefix": "FORM#"
        }
    )

    return success({"forms": result.get("Items", [])})


def delete_form(event):
    user_id     = _get_user_id(event)
    path_params = event.get("pathParameters") or {}
    form_id     = path_params.get("formId")

    if not user_id:
        return error("Unauthorized", 401)
    if not form_id:
        return error("formId is required")

    table = get_table()
    table.delete_item(Key={
        "PK": f"USER#{user_id}",
        "SK": f"FORM#{form_id}"
    })

    return success({"message": "Form deleted"})