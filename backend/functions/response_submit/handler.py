import json
import uuid
import os
from datetime import datetime, timezone

from db import get_table
from response import success, error

def lambda_handler(event, context):
    path_params = event.get("pathParameters") or {}
    form_id     = path_params.get("formId")

    if not form_id:
        return error("formId is required")

    body    = json.loads(event.get("body") or "{}")
    answers = body.get("answers", {})

    if not answers:
        return error("answers are required")

    response_id = str(uuid.uuid4())
    now         = datetime.now(timezone.utc).isoformat()

    table = get_table()

    # Verify form exists first
    form_check = table.query(
        IndexName="GSI1",
        KeyConditionExpression="GSI1PK = :pk AND GSI1SK = :sk",
        ExpressionAttributeValues={
            ":pk": f"FORM#{form_id}",
            ":sk": "METADATA"
        }
    )

    if not form_check.get("Items"):
        return error("Form not found", 404)

    table.put_item(Item={
        "PK":          f"FORM#{form_id}",
        "SK":          f"RESPONSE#{response_id}",
        "GSI1PK":      f"FORM#{form_id}",
        "GSI1SK":      f"RESPONSE#{response_id}",
        "formId":      form_id,
        "responseId":  response_id,
        "answers":     answers,
        "submittedAt": now,
    })

    return success({"responseId": response_id}, 201)