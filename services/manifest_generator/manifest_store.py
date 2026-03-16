import os
from typing import Any, Dict

import boto3


DYNAMODB_TABLE = os.environ.get("MANIFEST_TABLE", "UNKNOWN")
dynamodb = boto3.resource("dynamodb")


def get_table():
    """
    Return the DynamoDB table resource for manifest storage.

    This is controlled scaffolding only.
    """
    return dynamodb.Table(DYNAMODB_TABLE)


def save_manifest(manifest: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save a manifest document to DynamoDB.

    Placeholder persistence implementation:
    - writes the manifest as a single item
    - assumes manifest_id is the partition key
    """
    table = get_table()
    table.put_item(Item=manifest)
    return {"status": "saved", "manifest_id": manifest.get("manifest_id", "UNKNOWN")}


def load_manifest(manifest_id: str) -> Dict[str, Any]:
    """
    Load a manifest from DynamoDB by manifest_id.

    Placeholder read implementation.
    """
    table = get_table()
    response = table.get_item(Key={"manifest_id": manifest_id})
    return response.get("Item", {})
