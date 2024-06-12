from fastapi import UploadFile


class MLServices:
    def __init__(self):
        self.model_path = "model_path"  # TODO

    def do_translation(self, file: UploadFile) -> str:
        # TODO
        return "translation_text"
