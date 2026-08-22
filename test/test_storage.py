import pytest
from botocore.exceptions import ClientError

from src.exceptions import StorageError
from src.storage import PDFStorage


class _FakeS3Client:
    def __init__(self, bucket_exists=True, put_error=None):
        self._bucket_exists = bucket_exists
        self._put_error = put_error
        self.created_buckets = []
        self.put_calls = []

    def head_bucket(self, Bucket):
        if not self._bucket_exists:
            raise ClientError({"Error": {"Code": "404", "Message": "Not Found"}}, "HeadBucket")

    def create_bucket(self, Bucket):
        self.created_buckets.append(Bucket)

    def put_object(self, Bucket, Key, Body):
        if self._put_error:
            raise self._put_error
        self.put_calls.append((Bucket, Key, Body))


def test_store_uploads_object_and_returns_key(monkeypatch):
    fake_client = _FakeS3Client(bucket_exists=True)
    monkeypatch.setattr("src.storage._client", lambda: fake_client)

    key = PDFStorage.store(b"hello world", "my document.pdf")

    assert key.endswith("my document.pdf")
    assert len(fake_client.put_calls) == 1
    _bucket, put_key, body = fake_client.put_calls[0]
    assert body == b"hello world"
    assert put_key == key
    assert fake_client.created_buckets == []  # bucket already existed, no create call


def test_store_creates_bucket_if_missing(monkeypatch):
    fake_client = _FakeS3Client(bucket_exists=False)
    monkeypatch.setattr("src.storage._client", lambda: fake_client)

    PDFStorage.store(b"data", "doc.pdf")

    assert fake_client.created_buckets == ["pdf-summarizer-documents"]


def test_store_raises_storage_error_on_upload_failure(monkeypatch):
    error = ClientError({"Error": {"Code": "500", "Message": "boom"}}, "PutObject")
    fake_client = _FakeS3Client(bucket_exists=True, put_error=error)
    monkeypatch.setattr("src.storage._client", lambda: fake_client)

    with pytest.raises(StorageError):
        PDFStorage.store(b"data", "doc.pdf")


def test_store_generates_unique_keys_for_same_filename(monkeypatch):
    fake_client = _FakeS3Client(bucket_exists=True)
    monkeypatch.setattr("src.storage._client", lambda: fake_client)

    key1 = PDFStorage.store(b"data", "doc.pdf")
    key2 = PDFStorage.store(b"data", "doc.pdf")

    assert key1 != key2


def test_store_strips_path_from_filename(monkeypatch):
    """A file opened via open('/tmp/upload.pdf').name is a full path -- the
    S3 key must not embed slashes from it, or S3 treats it as a pseudo-directory."""
    fake_client = _FakeS3Client(bucket_exists=True)
    monkeypatch.setattr("src.storage._client", lambda: fake_client)

    key = PDFStorage.store(b"data", "/tmp/sample.pdf")

    assert "/" not in key
    assert key.endswith("sample.pdf")
