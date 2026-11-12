import requests
from datetime import datetime, timedelta

from config import BASE_URL, TOKEN_TTL_MINUTES, REQUEST_TIMEOUT
from exceptions import RediafileError
from account import AccountMixin
from files import FilesMixin
from folders import FoldersMixin


class _BaseClient:
    """Авторизация и универсальные запросы. Остальное — в миксинах."""

    def __init__(self, username=None, password=None, key1=None, key2=None,
                 base_url=BASE_URL, timeout=REQUEST_TIMEOUT):
        if not ((username and password) or (key1 and key2)):
            raise ValueError("Нужно указать либо username/password, либо key1/key2")

        self.username = username
        self.password = password
        self.key1 = key1
        self.key2 = key2

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.access_token = None
        self.account_id = None
        self._token_expires_at = None
        self.session = requests.Session()

    def _ensure_auth(self):
        if self.access_token and self._token_expires_at \
                and datetime.now() < self._token_expires_at:
            return

        payload = {}
        if self.key1 and self.key2:
            payload["key1"] = self.key1
            payload["key2"] = self.key2
        else:
            payload["username"] = self.username
            payload["password"] = self.password

        resp = self.session.post(
            f"{self.base_url}/authorize", data=payload, timeout=self.timeout
        )
        data = resp.json()
        if data.get("_status") != "success":
            raise RediafileError(f"Ошибка авторизации: {data.get('response', data)}")

        self.access_token = data["data"]["access_token"]
        self.account_id = str(data["data"]["account_id"])
        self._token_expires_at = datetime.now() + timedelta(minutes=TOKEN_TTL_MINUTES)

    def _post(self, endpoint, data=None, files=None):
        self._ensure_auth()
        payload = {
            "access_token": self.access_token,
            "account_id": self.account_id,
        }
        if data:
            payload.update(data)

        resp = self.session.post(
            f"{self.base_url}/{endpoint}",
            data=payload, files=files, timeout=self.timeout,
        )
        result = resp.json()
        if result.get("_status") not in ("success", "successful"):
            raise RediafileError(
                f"Rediafile API error ({endpoint}): "
                f"{result.get('response', result)}"
            )
        return result

    def disable_token(self):
        """POST /disable_access_token — досрочно деактивировать токен."""
        return self._post("disable_access_token")


class RediafileClient(AccountMixin, FilesMixin, FoldersMixin, _BaseClient):
    """
    Единая точка входа. Методы собираются из миксинов:
      - AccountMixin: работа с аккаунтом
      - FilesMixin:   файлы
      - FoldersMixin: папки
      - _BaseClient:  авторизация, _post, disable_token
    """
    pass