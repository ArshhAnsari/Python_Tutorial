from datetime import datetime
import json
import os
import time
from functools import wraps

DATA_FILE = r"C:\Users\Mohd Arsh\Python_Workspace\7_Problems\bank_data.json"


# DECORATORS
def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] Finished {func.__name__}")
        return result
    return wrapper


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] {func.__name__} took {end - start:.6f} sec")
        return result
    return wrapper


# CLASSES
class Customer:
    all_customers = {}

    def __init__(self, customer_id, name, email, phone_no):
        self._customer_id = customer_id
        self.name = name
        self.email = email
        self.phone_no = phone_no
        self.accounts = []

    @property
    def customer_id(self):
        return self._customer_id

    def display(self):
        print(f"ID: {self.customer_id}, Name: {self.name}, Email: {self.email}, Phone: {self.phone_no}")

    def add_account(self, account):
        self.accounts.append(account)

    def show_accounts(self):
        if not self.accounts:
            print("No accounts found for this customer")
            return
        print(f"\nAccounts of {self.name}:")
        for acc in self.accounts:
            acc.display()

    @classmethod
    def register(cls, customer_id, name, email, phone_no):
        if customer_id in cls.all_customers:
            print("Duplicate customer ID. Registration Failed!")
            return None
        customer = cls(customer_id, name, email, phone_no)
        cls.all_customers[customer_id] = customer
        print("Customer registered successfully")
        return customer

    @classmethod
    def search(cls, customer_id):
        customer = cls.all_customers.get(customer_id)
        if customer:
            customer.display()
            return customer
        print("Customer not found.")
        return None

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone_no": self.phone_no
        }


class Transcation:
    next_transaction_id = 1
    all_transcations = {}

    def __init__(self, tx_type, amount, account_no, balance_after, timestamp=None, transaction_id=None):
        if transaction_id is None:
            self.transaction_id = Transcation.next_transaction_id
            Transcation.next_transaction_id += 1
        else:
            self.transaction_id = transaction_id

        self.type = tx_type
        self.amount = amount
        self.account_no = account_no
        self.balance_after = balance_after
        self.timestamp = timestamp if timestamp else datetime.now()

        Transcation.all_transcations[self.transaction_id] = self

    def display(self):
        ts = self.timestamp
        if isinstance(ts, str):
            ts_text = ts
        else:
            ts_text = ts.strftime('%Y-%m-%d %H:%M:%S')

        print(
            f"TX ID: {self.transaction_id} | "
            f"{self.type.upper()} | "
            f"Amount: {self.amount} | "
            f"Balance After: {self.balance_after} | "
            f"Time: {ts_text}"
        )

    def to_dict(self):
        ts = self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else str(self.timestamp)
        return {
            "transaction_id": self.transaction_id,
            "type": self.type,
            "amount": self.amount,
            "account_no": self.account_no,
            "balance_after": self.balance_after,
            "timestamp": ts
        }


class Account:
    next_acc_no = 1001
    all_accounts = {}

    def __init__(self, customer, balance=0, account_no=None):
        if not isinstance(customer, Customer):
            raise TypeError("Account must be linked to a Customer")
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")

        if account_no is None:
            self.account_no = Account.next_acc_no
            Account.next_acc_no += 1
        else:
            self.account_no = account_no

        self.customer = customer
        self._balance = balance
        self.transactions = []

        Account.all_accounts[self.account_no] = self
        customer.add_account(self)

    @property
    def balance(self):
        return self._balance

    def _record_transaction(self, tx_type, amount):
        tx = Transcation(tx_type, amount, self.account_no, self._balance)
        self.transactions.append(tx)
        return tx

    def display(self):
        print(
            f"Account No: {self.account_no}, "
            f"Type: {self.__class__.__name__}, "
            f"Balance: {self._balance}, "
            f"Customer: {self.customer.name}"
        )

    @logger
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self._record_transaction("deposit", amount)
            print(f"Deposited {amount}. New Balance: {self._balance}")
            return True
        print("Deposit amount must be positive.")
        return False

    @logger
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if amount > self._balance:
            print("Insufficient balance.")
            return False

        self._balance -= amount
        self._record_transaction("withdraw", amount)
        print(f"Withdrawn {amount}. New Balance: {self._balance}")
        return True

    def show_statement(self):
        print(f"\n--- Statement for Account {self.account_no} ---")
        if not self.transactions:
            print("No transactions yet.")
            return
        for tx in self.transactions:
            tx.display()
        print(f"Current Balance: {self._balance}")
        print("------------------------------------------")

    @logger
    @timer
    def transfer(self, from_account, to_account, amount):
        if not isinstance(from_account, Account) or not isinstance(to_account, Account):
            print("Transfer failed: both must be valid Account objects.")
            return False

        if from_account is to_account or from_account.account_no == to_account.account_no:
            print("Transfer failed: cannot transfer to the same account.")
            return False

        if amount <= 0:
            print("Transfer failed: amount must be positive.")
            return False

        success = from_account.withdraw(amount)
        if not success:
            print("Transfer failed: withdrawal from source account was not possible.")
            return False

        deposited = to_account.deposit(amount)
        if not deposited:
            print("Transfer failed: deposit into target account failed.")
            return False

        print(
            f"Transfer successful: {amount} moved from "
            f"Account {from_account.account_no} to Account {to_account.account_no}"
        )
        return True

    def to_dict(self):
        return {
            "account_no": self.account_no,
            "type": self.__class__.__name__,
            "balance": self._balance,
            "customer_id": self.customer.customer_id
        }


class SavingsAccount(Account):
    interest_rate = 0.04

    def add_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        self._record_transaction("interest", interest)
        print(f"Interest added: {interest}. New Balance: {self._balance}")


class CurrentAccount(Account):
    overdraft_limit = 5000

    @logger
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if amount > self._balance + self.overdraft_limit:
            print("Overdraft limit exceeded.")
            return False

        self._balance -= amount
        self._record_transaction("withdraw", amount)
        print(f"Withdrawn {amount}. New Balance: {self._balance}")
        return True


class BusinessAccount(Account):
    transaction_fee = 20

    @logger
    def withdraw(self, amount):
        total = amount + self.transaction_fee
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if total > self._balance:
            print("Insufficient balance including transaction fee.")
            return False

        self._balance -= total
        self._record_transaction("withdraw", amount)
        print(f"Withdrawn {amount} + fee {self.transaction_fee}. New Balance: {self._balance}")
        return True


# GENERATORS
def iter_transactions(account):
    for tx in account.transactions:
        yield tx


def iter_transactions_by_type(account, tx_type):
    for tx in account.transactions:
        if tx.type == tx_type:
            yield tx


# REPORTS
@logger
@timer
def find_highest_balance_account():
    if not Account.all_accounts:
        print("No accounts available.")
        return None

    highest = max(Account.all_accounts.values(), key=lambda acc: acc.balance)
    print("\n--- Highest Balance Account ---")
    highest.display()
    return highest


@logger
def summarize_transactions(account):
    summary = {
        "deposit_count": 0,
        "deposit_total": 0.0,
        "withdraw_count": 0,
        "withdraw_total": 0.0,
        "interest_count": 0,
        "interest_total": 0.0,
        "total_transactions": 0
    }

    for tx in iter_transactions(account):
        summary["total_transactions"] += 1
        if tx.type == "deposit":
            summary["deposit_count"] += 1
            summary["deposit_total"] += tx.amount
        elif tx.type == "withdraw":
            summary["withdraw_count"] += 1
            summary["withdraw_total"] += tx.amount
        elif tx.type == "interest":
            summary["interest_count"] += 1
            summary["interest_total"] += tx.amount

    print(f"\n--- Transaction Summary for Account {account.account_no} ---")
    print(f"Total transactions : {summary['total_transactions']}")
    print(f"Deposits           : {summary['deposit_count']} | Amount: {summary['deposit_total']}")
    print(f"Withdrawals        : {summary['withdraw_count']} | Amount: {summary['withdraw_total']}")
    print(f"Interest entries   : {summary['interest_count']} | Amount: {summary['interest_total']}")
    return summary


@logger
def generate_statement(account):
    print(f"\n--- Generated Statement for Account {account.account_no} ---")
    if not account.transactions:
        print("No transactions found.")
        return

    for tx in iter_transactions(account):
        tx.display()
    print(f"Available Balance: {account.balance}")


@logger
def calculate_educational_interest(account):
    if not isinstance(account, SavingsAccount):
        print("Interest calculation is only for Savings accounts.")
        return 0

    interest = account.balance * SavingsAccount.interest_rate
    print(
        f"Educational interest for Account {account.account_no}: "
        f"{interest} (rate={SavingsAccount.interest_rate})"
    )
    return interest


@logger
@timer
def full_bank_report():
    print("\n" + "=" * 45)
    print("           BANK REPORT")
    print("=" * 45)
    print(f"Total customers     : {len(Customer.all_customers)}")
    print(f"Total accounts      : {len(Account.all_accounts)}")
    print(f"Total transactions  : {len(Transcation.all_transcations)}")

    find_highest_balance_account()

    print("\n--- Account-wise Summary ---")
    for acc in Account.all_accounts.values():
        acc.display()
        summarize_transactions(acc)


# PERSISTENCE LAYER
def save_data(filename=DATA_FILE):
    data = {
        "customers": [c.to_dict() for c in Customer.all_customers.values()],
        "accounts": [a.to_dict() for a in Account.all_accounts.values()],
        "transactions": [t.to_dict() for t in Transcation.all_transcations.values()],
        "next_acc_no": Account.next_acc_no,
        "next_transaction_id": Transcation.next_transaction_id
    }
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")


def load_data(filename=DATA_FILE):
    if not os.path.exists(filename):
        print("No saved data found. Starting fresh.")
        return

    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Data file is malformed. Starting fresh.")
        return
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    Customer.all_customers.clear()
    Account.all_accounts.clear()
    Transcation.all_transcations.clear()

    for c in data.get("customers", []):
        customer = Customer(
            c["customer_id"],
            c["name"],
            c["email"],
            c["phone_no"]
        )
        Customer.all_customers[customer.customer_id] = customer

    type_map = {
        "SavingsAccount": SavingsAccount,
        "CurrentAccount": CurrentAccount,
        "BusinessAccount": BusinessAccount,
        "Account": Account
    }

    for a in data.get("accounts", []):
        customer = Customer.all_customers.get(a["customer_id"])
        if not customer:
            continue
        cls = type_map.get(a["type"], Account)
        cls(customer, a["balance"], account_no=a["account_no"])

    for t in data.get("transactions", []):
        tx = Transcation(
            t["type"],
            t["amount"],
            t["account_no"],
            t["balance_after"],
            timestamp=t.get("timestamp"),
            transaction_id=t["transaction_id"]
        )
        account = Account.all_accounts.get(t["account_no"])
        if account:
            account.transactions.append(tx)

    Account.next_acc_no = data.get("next_acc_no", Account.next_acc_no)
    Transcation.next_transaction_id = data.get("next_transaction_id", Transcation.next_transaction_id)

    print("Data loaded successfully.")


# ============================================================
# MENU / APPLICATION FLOW
# ============================================================

def get_account_by_no(account_no):
    return Account.all_accounts.get(account_no)


def main():
    load_data()

    while True:
        print("\n" + "=" * 45)
        print("         BANK MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1.  Register Customer")
        print("2.  Create Account")
        print("3.  Deposit")
        print("4.  Withdraw")
        print("5.  Transfer")
        print("6.  Search Customer")
        print("7.  Show Accounts of Customer")
        print("8.  Show Statement")
        print("9.  Save Data")
        print("10. Highest Balance Account")
        print("11. Account Transaction Summary")
        print("12. Generate Statement (Report)")
        print("13. Calculate Educational Interest")
        print("14. Full Bank Report")
        print("15. Exit")
        print("=" * 45)

        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                cid = int(input("Customer ID: "))
                name = input("Name: ").strip()
                email = input("Email: ").strip()
                phone = input("Phone: ").strip()
                Customer.register(cid, name, email, phone)
                save_data()

            elif choice == "2":
                cid = int(input("Customer ID: "))
                customer = Customer.all_customers.get(cid)
                if not customer:
                    print("Customer not found.")
                    continue

                print("Account Type: 1.Savings  2.Current  3.Business")
                t = input("Choose type: ").strip()
                balance = float(input("Initial balance: "))

                if t == "1":
                    SavingsAccount(customer, balance)
                elif t == "2":
                    CurrentAccount(customer, balance)
                elif t == "3":
                    BusinessAccount(customer, balance)
                else:
                    print("Invalid account type.")
                    continue

                print("Account created.")
                save_data()

            elif choice == "3":
                acc_no = int(input("Account No: "))
                amount = float(input("Amount: "))
                acc = get_account_by_no(acc_no)
                if not acc:
                    print("Account not found.")
                    continue
                if acc.deposit(amount):
                    save_data()

            elif choice == "4":
                acc_no = int(input("Account No: "))
                amount = float(input("Amount: "))
                acc = get_account_by_no(acc_no)
                if not acc:
                    print("Account not found.")
                    continue
                if acc.withdraw(amount):
                    save_data()

            elif choice == "5":
                from_no = int(input("From Account No: "))
                to_no = int(input("To Account No: "))
                amount = float(input("Amount: "))
                from_acc = get_account_by_no(from_no)
                to_acc = get_account_by_no(to_no)
                if not from_acc or not to_acc:
                    print("One or both accounts not found.")
                    continue
                if from_acc.transfer(from_acc, to_acc, amount):
                    save_data()

            elif choice == "6":
                cid = int(input("Customer ID: "))
                Customer.search(cid)

            elif choice == "7":
                cid = int(input("Customer ID: "))
                customer = Customer.all_customers.get(cid)
                if customer:
                    customer.show_accounts()
                else:
                    print("Customer not found.")

            elif choice == "8":
                acc_no = int(input("Account No: "))
                acc = get_account_by_no(acc_no)
                if not acc:
                    print("Account not found.")
                    continue
                acc.show_statement()

            elif choice == "9":
                save_data()

            elif choice == "10":
                find_highest_balance_account()

            elif choice == "11":
                acc_no = int(input("Account No: "))
                acc = get_account_by_no(acc_no)
                if not acc:
                    print("Account not found.")
                    continue
                summarize_transactions(acc)

            elif choice == "12":
                acc_no = int(input("Account No: "))
                acc = get_account_by_no(acc_no)
                if not acc:
                    print("Account not found.")
                    continue
                generate_statement(acc)

            elif choice == "13":
                acc_no = int(input("Account No: "))
                acc = get_account_by_no(acc_no)
                if not acc:
                    print("Account not found.")
                    continue
                calculate_educational_interest(acc)

            elif choice == "14":
                full_bank_report()

            elif choice == "15":
                save_data()
                print("Exiting... Data saved.")
                break

            else:
                print("Invalid choice.")

        except ValueError:
            print("Invalid input. Please enter correct values.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()