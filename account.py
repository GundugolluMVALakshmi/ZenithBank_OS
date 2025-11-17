# account.py
import time

class Account:
    def __init__(self, username: str, password: str, balance: float, meta: dict):
        self.username = username
        self.password = password
        self.balance = balance
        self._meta = meta
        self._transactions = []

    def verify(self, pwd: str) -> bool:
        return pwd == self.password

    def deposit(self, amt: float):
        if amt <= 0:
            return "Deposit must be greater than 0."
        self.balance += amt
        self._transactions.append(f"{time.ctime()}: Deposited ₹{amt}")
        return f"Deposit successful. New balance ₹{self.balance}"

    def withdraw(self, amt: float):
        if amt <= 0:
            return "Amount must be greater than 0."
        if amt > self.balance:
            return "Insufficient balance."
        self.balance -= amt
        self._transactions.append(f"{time.ctime()}: Withdrawn ₹{amt}")
        return f"Withdrawal successful. New balance ₹{self.balance}"

    def get_balance_str(self):
        return f"Current Balance: ₹{self.balance}"

    def get_transactions(self, n=50):
        return self._transactions[-n:]
