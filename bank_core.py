# bank_core.py
import os
import json
from account import Account

BASE_DIR = os.path.dirname(__file__)
USER_DIR = os.path.join(BASE_DIR, "data", "users")
os.makedirs(USER_DIR, exist_ok=True)

class BankCore:
    def __init__(self):
        pass

    def _user_file(self, username):
        return os.path.join(USER_DIR, f"{username}.json")

    def register(self, username, password, initial_amount=0):
        path = self._user_file(username)
        if os.path.exists(path):
            return False, "Username already exists."

        data = {
            "username": username,
            "password": password,
            "balance": float(initial_amount),
            "meta": {"account_no": f"AC-{hash(username)%1000000}"}
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return True, "Registration successful!"

    def authenticate(self, username, password):
        path = self._user_file(username)
        if not os.path.exists(path):
            return False

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data["password"] == password

    def get_account(self, username):
        path = self._user_file(username)
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        acc = Account(
            username=data["username"],
            password=data["password"],
            balance=data["balance"],
            meta=data["meta"]
        )

        return acc
