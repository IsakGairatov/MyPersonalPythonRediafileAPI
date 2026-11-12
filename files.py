import base64


class FilesMixin:
    def upload_file(self, file_path, folder_id=None):
        """POST /file/upload — загрузка локального файла."""
        with open(file_path, "rb") as f:
            files = {"upload_file": f}
            data = {}
            if folder_id:
                data["folder_id"] = str(folder_id)
            return self._post("file/upload", data=data, files=files)

    def download_link(self, file_id):
        """POST /file/download — ссылка на скачивание."""
        return self._post("file/download", data={"file_id": str(file_id)})

    def file_info(self, file_id):
        """POST /file/info — метаданные файла."""
        return self._post("file/info", data={"file_id": str(file_id)})

    def edit_file(self, file_id, filename=None, file_type=None, folder_id=None):
        """POST /file/edit — переименование / изменение метаданных."""
        data = {"file_id": str(file_id)}
        if filename is not None:
            data["filename"] = filename
        if file_type is not None:
            data["fileType"] = file_type
        if folder_id is not None:
            data["folder_id"] = str(folder_id)
        return self._post("file/edit", data=data)

    def delete_file(self, file_id):
        """POST /file/delete — в корзину."""
        return self._post("file/delete", data={"file_id": str(file_id)})

    def move_file(self, file_id, new_parent_folder_id):
        """POST /file/move."""
        return self._post("file/move", data={
            "file_id": str(file_id),
            "new_parent_folder_id": str(new_parent_folder_id),
        })

    def copy_file(self, file_id, copy_to_folder_id):
        """POST /file/copy."""
        return self._post("file/copy", data={
            "file_id": str(file_id),
            "copy_to_folder_id": str(copy_to_folder_id),
        })

    def url_upload_add(self, url, folder_id=None):
        """POST /file/url_upload_add — загрузка по внешнему URL (base64)."""
        encoded = base64.b64encode(url.encode("utf-8")).decode("utf-8")
        data = {"file_url_base64": encoded}
        if folder_id:
            data["folder_id"] = str(folder_id)
        return self._post("file/url_upload_add", data=data)

    def url_upload_status(self, scheduled_item_id):
        """POST /file/url_upload_status — статус загрузки по URL."""
        return self._post("file/url_upload_status",
                          data={"scheduled_item_id": str(scheduled_item_id)})