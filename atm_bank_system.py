import math

class Account:
    max_attempts=3
    __counter=1001

    def __init__(self,holder,pin):
        if not Account.is_valid_pin(pin):
            raise ValueError("Pin must be exactly 4 digits")
        self.holder=holder
        self.account_no=Account.__counter
        Account.__counter+=1
        self.__pin=pin
        self.__balance=0
        self.__fail_attempts=0
        self.__lock=False

    def __str__(self):
        return f"{self.account_no} - {self.holder} - {self.__balance}"
    
    @staticmethod
    def is_valid_pin(pin):
        return pin.isdigit() and len(pin) == 4

    @property
    def balance(self):
        return self.__balance
    
    @property
    def locked(self):
        return self.__lock

    @property
    def attempts_left(self):
        return self.max_attempts-self.__fail_attempts

    def unlock(self):
        self.__lock=False
        self.__fail_attempts=0

    def verify_pin(self, p):
        if self.__lock:
            return False
        if p==self.__pin:
            self.__fail_attempts=0     
            return True
        self.__fail_attempts += 1
        if self.__fail_attempts>=Account.max_attempts:
            self.__lock=True
        return False

    def __check_amount(self, amount):
        if not math.isfinite(amount) or amount<=0:
            raise ValueError("Amount must be a positive number")

    
    def deposit(self,amount):
        self.__check_amount(amount)
        self.__balance=self.__balance + amount

    def change_pin(self,old_pin,new_pin):
        if self.__lock:
            raise ValueError("Account is locked")
        if not self.verify_pin(old_pin):
            raise ValueError("Invalid old pin")
        if not Account.is_valid_pin(new_pin):
            raise ValueError("New pin must be exactly 4 digits")
        self.__pin=new_pin
        

    def withdraw(self,amount):
        self.__check_amount(amount)
        if amount>self.__balance:
            raise ValueError("Insufficient funds!")
        self.__balance=self.__balance-amount
            
class Bank:
    Admin_pin="0000"      

    def __init__(self):
        self.accounts={}   

    def __find(self, account_no):
        if account_no not in self.accounts:
            raise ValueError("No such account!")
        return self.accounts[account_no]
        

    def create_account(self, holder, pin):
        name=holder.strip()
        if name=="":
            raise ValueError("Please enter holder name")
        acc=Account(name,pin)
        self.accounts[acc.account_no] = acc
        return acc

    def login(self, account_no, pin):
        account=self.__find(account_no)
        if account.locked:
            raise ValueError("Too many wrong attempts, Account locked.")
        if account.verify_pin(pin):
            return account
        raise ValueError(f"Invalid pin. Attempts left: {account.attempts_left}")

    def admin_unlock(self, account_no, admin_pin):
        if admin_pin!=Bank.Admin_pin: 
            raise ValueError("Invalid admin pin")
        account = self.__find(account_no)
        account.unlock()             
        
def ask_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Enter interger value only!")
        return None
    
def ask_pin(prompt):
    return input(prompt)

def ask_amount(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        print("Enter value correctly")
        return None

def acc_menu(acc):
    while True:
        print(f"\nwelcome {acc.holder}")
        print("1.deposit   2.withdraw   3.check balance  4.change pin  5.exit")      
        ch=ask_int("enter your choice: ")
        match ch:
            case 1:
                amount=ask_amount("Enter amount: ")
                if amount is None:
                    continue
                try:
                    acc.deposit(amount)
                    print("Deposit successful!")
                except ValueError as e:
                    print(e)
            case 2:
                amount=ask_amount("Enter amount: ")
                if amount is None:
                    continue
                try:
                    acc.withdraw(amount)
                    print("withdrawl successful!")
                except ValueError as e:
                    print(e)
            case 3:
                print(f"your balance: Rs {acc.balance:.2f}")
            case 4:
                old_pin=ask_pin("Enter old pin: ")
                new_pin=ask_pin("Enter new pin: ")
                try:
                    acc.change_pin(old_pin,new_pin)
                    print("Pin updated successfully")
                except ValueError as e:
                    print(e)
            case 5:
                print("Exitting")
                break
            case _:
                print("Invalid choice!")

bank=Bank()

while True:
    print("\nBANK")
    print("1.create account  2.login  3.admin unlock  4.exit")
    ch=ask_int("enter your choice: ")
    match ch:
        case 1:
            name=input("Enter holder name: ")
            pin=ask_pin("Enter pin: ")
            try:
                acc=bank.create_account(name,pin)
                print("Account created successfully!")
                print("Your account number is:", acc.account_no)
            except ValueError as e:
                print(e)
        case 2:
            acc_no=ask_int("Enter account no.: ")
            pin=ask_pin("Enter pin: ")
            try:
                acc=bank.login(acc_no,pin)
                acc_menu(acc)
            except ValueError as e:
                print(e)
        case 3:
            acc_no=ask_int("Enter account no.: ")
            admin_pin=ask_pin("Enter admin pin: ")
            try:
                bank.admin_unlock(acc_no,admin_pin)
                print("Account unlocked")
            except ValueError as e:
                print(e)
        case 4:
            print("Exitting")
            break
        case _:
            print("Invalid choice!")