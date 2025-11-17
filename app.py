# app.py
"""
ZenithBank OS - Console UI
Run: python app.py
"""
from __future__ import annotations
import os
import sys
import time
import getpass
from bank_core import BankCore
from account import Account
from utils import safe_float
from typing import Optional

BC = BankCore()

BANNER = r"""
==================================================
           Z E N I T H B A N K   O S
   Multi-User Banking Operating System (Python)
==================================================
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(msg="Press Enter to continue..."):
    input(msg)

def main_menu():
    while True:
        clear()
        print(BANNER)
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            login_flow()
        elif choice == "2":
            register_flow()
        elif choice == "3":
            print("Exiting ZenithBank OS. Goodbye.")
            sys.exit(0)
        else:
            print("Invalid choice.")
            pause()

def register_flow():
    clear()
    print("--- Register New Account ---")
    username = input("Choose username: ").strip()
    if not username:
        print("Username cannot be empty.")
        pause()
        return
    password = getpass.getpass("Set a password: ").strip()
    if not password:
        print("Password cannot be empty.")
        pause()
        return
    initial = input("Initial deposit (press Enter for 0): ").strip()
    initial_val = safe_float(initial, 0.0)
    ok, msg = BC.register(username, password, initial_val)
    print(msg)
    pause()

def login_flow():
    clear()
    print("--- Login ---")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()
    if BC.authenticate(username, password):
        account = BC.get_account(username)
        print(f"Login successful. Welcome {username}!")
        pause()
        user_session(account)
    else:
        print("Invalid credentials.")
        pause()

def user_session(account: Account):
    while True:
        clear()
        print(BANNER)
        print(account.get_balance_str())
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Export Statement")
        print("6. Logout")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            deposit_flow(account)
        elif choice == "2":
            withdraw_flow(account)
        elif choice == "3":
            print(account.get_balance_str())
            pause()
        elif choice == "4":
            txs = account.get_transactions(100)
            if not txs:
                print("No transactions yet.")
            else:
                print("\n".join(txs[-50:]))
            pause()
        elif choice == "5":
            export_statement(account)
            pause()
        elif choice == "6":
            print("Logging out...")
            time.sleep(0.6)
            break
        else:
            print("Invalid choice.")
            pause()

def deposit_flow(account: Account):
    amt = input("Enter deposit amount: ").strip()
    val = safe_float(amt, None)
    if val is None:
        print("Invalid amount.")
        pause()
        return
    print(account.deposit(val))
    pause()

def withdraw_flow(account: Account):
    amt = input("Enter withdrawal amount: ").strip()
    val = safe_float(amt, None)
    if val is None:
        print("Invalid amount.")
        pause()
        return
    print(account.withdraw(val))
    pause()

def export_statement(account: Account):
    # Simple text statement
    username = account.username
    meta = account._meta
    accno = meta.get("account_no", "UNKNOWN")
    lines = []
    lines.append("ZENITHBANK OS - Account Statement")
    lines.append(f"Account Holder: {username}")
    lines.append(f"Account No: {accno}")
    lines.append("-" * 40)
    txs = account.get_transactions(1000)
    if not txs:
        lines.append("No transactions.")
    else:
        lines.extend(txs)
    lines.append("-" * 40)
    lines.append(account.get_balance_str())
    out_dir = os.path.join(os.path.dirname(__file__), "data", "users", username)
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f"statement_{username}_{int(time.time())}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Statement exported: {filename}")

if __name__ == "__main__":
    main_menu()
