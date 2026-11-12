class AccountMixin:
    def get_account_info(self):
        """POST /account/info — информация об аккаунте."""
        return self._post("account/info")

    def get_account_package(self):
        """POST /account/package — лимиты и ограничения тарифа."""
        return self._post("account/package")