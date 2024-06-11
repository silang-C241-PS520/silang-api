import uuid

from fastapi import UploadFile
from google.cloud import storage


class GCPStorageServices:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_name = "silang-c241-ps520-dev"  # TODO: jadiin variable

    def upload_file(self, file: UploadFile) -> str:
        bucket = self.storage_client.bucket(self.bucket_name)
        randomize_file_name = uuid.uuid4().hex
        file_path = f"videos/{randomize_file_name}"
        blob = bucket.blob(file_path)
        blob.upload_from_file(file.file, content_type=file.content_type)  # TODO content_types nya apa? mp4? ato ngikutin file yg diupload?
        return f"https://storage.googleapis.com/{self.bucket_name}/{file_path}"
