Well, I tried to make library for rediafile-api to use this service, but it returns error for uploading right now (error from service side). Later I discovered this service is suspicious, so i changed my mind. 

Anyway if someone interested thats example of my code usage (RediafileAPI is the name of directory where this code is stored):


```import json

from RediafileAPI import RediafileClient, RediafileError

client = RediafileClient(key1="lpaWQ7jFQdpRVYyaOWxloJQ8A3C5WI7SxVBDtnZVwiMedvaGILghJmvvkoEmXEJy", key2="zJZNtV1HnVrdV9jyqGOqT6Fj6rZItE04BxoE7qjFZjmeeqQywr0AJ7VDZmxZEdmO")


try:
    # 1. Загрузка
    print("→ upload_file...")
    result = client.upload_file("text.txt")
    file_id = result["data"][0]["file_id"]
    print(f"  file_id = {file_id}")

    # 2. Переименование
    print("→ edit_file...")
    client.edit_file(file_id, filename="newname.txt")
    print("  переименовано")

    # 3. Получение ссылки
    print("→ download_link...")
    link = client.download_link(file_id)["data"]["download_url"]
    print(f"  link = {link}")

    # 4. Удаление
    print("→ delete_file...")
    client.delete_file(file_id)
    print("  удалено (в корзину)")

    print("\n✅ Все шаги прошли")

except RediafileError as e:
    print(f"\n❌ Ошибка Rediafile: {e}")
except Exception as e:
    print(f"\n❌ Неожиданная ошибка: {type(e).__name__}: {e}")```
