class FoldersMixin:
    def create_folder(self, folder_name, parent_id=None, is_public=0,
                      access_password_md5=None):
        """POST /folder/create. is_public: 0=Private, 1=Unlisted, 2=Public."""
        data = {"folder_name": folder_name, "is_public": is_public}
        if parent_id:
            data["parent_id"] = str(parent_id)
        if access_password_md5:
            data["access_password"] = access_password_md5
        return self._post("folder/create", data=data)

    def list_folder(self, parent_folder_id=None):
        """POST /folder/listing."""
        data = {}
        if parent_folder_id:
            data["parent_folder_id"] = str(parent_folder_id)
        return self._post("folder/listing", data=data)

    def folder_info(self, parent_folder_id=None):
        """POST /folder/info."""
        data = {}
        if parent_folder_id:
            data["parent_folder_id"] = str(parent_folder_id)
        return self._post("folder/info", data=data)

    def edit_folder(self, folder_id, folder_name=None, parent_id=None,
                    is_public=None, access_password_md5=None):
        """POST /folder/edit."""
        data = {"folder_id": str(folder_id)}
        if folder_name is not None:
            data["folder_name"] = folder_name
        if parent_id is not None:
            data["parent_id"] = str(parent_id)
        if is_public is not None:
            data["is_public"] = is_public
        if access_password_md5 is not None:
            data["access_password"] = access_password_md5
        return self._post("folder/edit", data=data)

    def delete_folder(self, folder_id):
        """POST /folder/delete."""
        return self._post("folder/delete", data={"folder_id": str(folder_id)})

    def move_folder(self, folder_id, new_parent_folder_id):
        """POST /folder/move."""
        return self._post("folder/move", data={
            "folder_id": str(folder_id),
            "new_parent_folder_id": str(new_parent_folder_id),
        })