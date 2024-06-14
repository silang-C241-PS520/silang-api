import os
import uuid

from fastapi import UploadFile
from google.cloud import storage

BUCKET_NAME = os.environ["BUCKET_NAME"]


class GCPStorageServices:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_name = BUCKET_NAME

    def __call__(self):
        return self

    def upload_file(self, temp_file_path: str) -> str:
        bucket = self.storage_client.bucket(self.bucket_name)
        randomize_file_name = uuid.uuid4().hex
        file_path = f"videos/{randomize_file_name}"
        blob = bucket.blob(file_path)
        blob.upload_from_filename(temp_file_path,
                                  content_type="video/mp4")  # TODO content_types nya apa? mp4? ato ngikutin file yg diupload?
        return f"https://storage.googleapis.com/{self.bucket_name}/{file_path}"
