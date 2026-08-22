"""Durable storage for uploaded PDFs, backed by LocalStack S3.

Store-first, then process: the raw upload is written to S3 before any
extraction/summarization work happens. This is deliberate — if downstream
processing fails, the original file isn't lost and can be reprocessed
without asking the user to re-upload. If the S3 write itself fails, the
whole request fails closed (see PDFStorage.store) rather than silently
processing a file with no durable record of it.
"""

import logging
import os
import uuid
from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from src.config import Config
from src.exceptions import StorageError

logger = logging.getLogger(__name__)


def _client():
    return boto3.client(
        "s3",
        endpoint_url=Config.S3_ENDPOINT_URL,
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.AWS_DEFAULT_REGION,
    )


def _ensure_bucket(client) -> None:
    try:
        client.head_bucket(Bucket=Config.S3_BUCKET_NAME)
    except ClientError:
        client.create_bucket(Bucket=Config.S3_BUCKET_NAME)


class PDFStorage:
    """Stores uploaded PDF bytes in S3 (LocalStack) before they're processed."""

    @staticmethod
    def store(data: bytes, filename: str) -> str:
        """Upload the given bytes to S3, returning the object key.

        Raises:
            StorageError: If the upload fails for any reason. Callers should
                treat this as fail-closed — do not proceed to process a file
                that couldn't be durably stored.
        """
        safe_filename = os.path.basename(filename) or "upload.pdf"
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        key = f"{timestamp}-{uuid.uuid4().hex[:8]}-{safe_filename}"

        try:
            client = _client()
            _ensure_bucket(client)
            client.put_object(Bucket=Config.S3_BUCKET_NAME, Key=key, Body=data)
        except (BotoCoreError, ClientError) as exc:
            raise StorageError(f"Failed to store uploaded PDF: {exc}") from exc

        logger.info("Stored uploaded PDF as s3://%s/%s (%d bytes)", Config.S3_BUCKET_NAME, key, len(data))
        return key
