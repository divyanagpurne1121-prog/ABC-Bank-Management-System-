import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import random
from datetime import datetime

FILE_NAME = "bank_data.json"

def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)

def load_data():

    if not os.path.exists(FILE_NAME):

        data = {
            "customers": [],
            "accounts": [],
            "transactions": [],
            "cards": [],
            "loans": [],
            "service_requests": []
        }

        save_data(data)
        return data

    with open(FILE_NAME, "r") as file:
        data = json.load(file)

    data.setdefault("customers", [])
    data.setdefault("accounts", [])
    data.setdefault("transactions", [])
    data.setdefault("cards", [])
    data.setdefault("loans", [])
    data.setdefault("service_requests", [])

    return data

data = load_data()
current_customer_id = None

def generate_customer_id():

    return "CUST" + str(len(data["customers"]) + 1).zfill(4)

def generate_account_number():

    return str(random.randint(1000000000, 9999999999))


def generate_card_number():

    return str(random.randint(1000000000000000, 9999999999999999))


def generate_request_id():

    return "REQ" + str(len(data["service_requests"]) + 1).zfill(4)


def generate_loan_id():

    return "LOAN" + str(len(data["loans"]) + 1).zfill(4)

def find_customer():

    for customer in data["customers"]:

        if customer["customer_id"] == current_customer_id:
            return customer

    return None


def find_account():

    for account in data["accounts"]:

        if account["customer_id"] == current_customer_id:
            return account

    return None


def clear_window():

    for widget in root.winfo_children():
        widget.destroy()


root = tk.Tk()

root.title("ABC Bank🏦 - Bank Management System")

root.geometry("950x650")

root.minsize(850, 600)


def create_title(text):

    title = tk.Label(
        root,
        text=text,
        font=("Arial", 24, "bold")
    )

    title.pack(pady=20)

    return title


def create_button(text, command, width=25):

    button = tk.Button(
        root,
        text=text,
        command=command,
        width=width,
        height=2,
        font=("Arial", 11)
    )

    return button


def home_page():

    clear_window()

    create_title("ABC BANK🏦")

    subtitle = tk.Label(
        root,
        text="Bank Management System",
        font=("Arial", 16)
    )

    subtitle.pack(pady=5)

    tk.Label(
        root,
        text="Welcome to ABC Bank",
        font=("Arial", 13)
    ).pack(pady=15)

    create_button(
        "Customer Registration",
        registration_page
    ).pack(pady=10)

    create_button(
        "Customer Login",
        login_page
    ).pack(pady=10)

    create_button(
        "Exit",
        root.destroy
    ).pack(pady=10)

def registration_page():

    clear_window()

    create_title("Customer Registration")

    frame = tk.Frame(root)
    frame.pack(pady=10)

    fields = [
        "Full Name",
        "Phone Number",
        "Email",
        "Address",
        "Password",
        "4-Digit PIN"
    ]

    entries = {}

    for i, field in enumerate(fields):

        tk.Label(
            frame,
            text=field + ":",
            font=("Arial", 11)
        ).grid(row=i, column=0, padx=10, pady=8, sticky="e")

        entry = tk.Entry(frame, width=35)

        if field in ["Password", "4-Digit PIN"]:
            entry.config(show="*")

        entry.grid(
            row=i,
            column=1,
            padx=10,
            pady=8
        )

        entries[field] = entry

    def register():

        name = entries["Full Name"].get().strip()
        phone = entries["Phone Number"].get().strip()
        email = entries["Email"].get().strip()
        address = entries["Address"].get().strip()
        password = entries["Password"].get()
        pin = entries["4-Digit PIN"].get()

        if not name or not phone or not email or not address:
            messagebox.showerror(
                "Error",
                "Please fill all fields."
            )
            return

        for customer in data["customers"]:

            if customer["phone"] == phone:

                messagebox.showerror(
                    "Error",
                    "Customer with this phone number already exists."
                )

                return

        if len(password) < 4:

            messagebox.showerror(
                "Error",
                "Password must contain at least 4 characters."
            )

            return

        if len(pin) != 4 or not pin.isdigit():

            messagebox.showerror(
                "Error",
                "PIN must contain exactly 4 digits."
            )

            return

        customer_id = generate_customer_id()

        account_number = generate_account_number()

        customer = {
            "customer_id": customer_id,
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
            "password": password,
            "pin": pin
        }

        data["customers"].append(customer)

        account = {
            "account_number": account_number,
            "customer_id": customer_id,
            "account_type": "Savings Account",
            "balance": 5000,
            "minimum_balance": 5000
        }

        data["accounts"].append(account)

        transaction = {
            "account_number": account_number,
            "type": "Account Opening",
            "amount": 5000,
            "date": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        }

        data["transactions"].append(transaction)

        save_data(data)

        messagebox.showinfo(
            "Registration Successful",
            "Customer registered successfully!\n\n"
            "Customer ID: " + customer_id +
            "\nAccount Number: " + account_number +
            "\nInitial Balance: Rs. 5000"
        )

        login_page()

    create_button(
        "Register",
        register
    ).pack(pady=10)

    create_button(
        "Back",
        home_page
    ).pack(pady=5)


def login_page():

    clear_window()

    create_title("Customer Login")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    tk.Label(
        frame,
        text="Phone Number:",
        font=("Arial", 11)
    ).grid(row=0, column=0, padx=10, pady=10)

    phone_entry = tk.Entry(
        frame,
        width=30
    )

    phone_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    tk.Label(
        frame,
        text="Password:",
        font=("Arial", 11)
    ).grid(row=1, column=0, padx=10, pady=10)

    password_entry = tk.Entry(
        frame,
        width=30,
        show="*"
    )

    password_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )

    def login():

        global current_customer_id

        phone = phone_entry.get().strip()
        password = password_entry.get()

        for customer in data["customers"]:

            if (
                customer["phone"] == phone
                and customer["password"] == password
            ):

                current_customer_id = customer["customer_id"]

                messagebox.showinfo(
                    "Login Successful",
                    "Welcome " + customer["name"]
                )

                customer_dashboard()

                return

        messagebox.showerror(
            "Login Failed",
            "Invalid phone number or password."
        )

    create_button(
        "Login",
        login
    ).pack(pady=10)

    create_button(
        "Back",
        home_page
    ).pack(pady=5)

def customer_dashboard():

    clear_window()

    root.geometry("1000x700")

    customer = find_customer()

    if customer is None:
        home_page()
        return


    title = tk.Label(
        root,
        text="🏦 ABC BANK",
        font=("Arial", 26, "bold")
    )
    title.pack(pady=10)

    welcome = tk.Label(
        root,
        text="Welcome, " + customer["name"],
        font=("Arial", 18, "bold")
    )
    welcome.pack(pady=5)

    tk.Label(
        root,
        text="Customer ID: " + customer["customer_id"],
        font=("Arial", 11)
    ).pack(pady=5)


    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)


    buttons = [

        ("💳 Account Details", account_details),

        ("💰 Deposit Money", deposit_money),

        ("🏧 Withdraw Money", withdraw_money),

        ("📜 Transaction History", transaction_history),

        ("💳 Debit / Credit Card", card_section),

        ("🏦 Loan Application", loan_section),

        ("📞 Customer Service", customer_service),

        ("🚪 Logout", logout)

    ]

    for i, (text, command) in enumerate(buttons):

        row = i // 2
        column = i % 2

        button = tk.Button(
            button_frame,
            text=text,
            command=command,
            width=32,
            height=2,
            font=("Arial", 12, "bold"),
            cursor="hand2"
        )

        button.grid(
            row=row,
            column=column,
            padx=20,
            pady=12
        )


    tk.Label(
        root,
        text="🏦 Banking Services:  💳 Cards   |   💰 Loans   |   📞 Customer Service:+91 892344421",
        font=("Arial", 12, "bold")
    ).pack(pady=10)


def account_details():

    account = find_account()

    if account is None:

        messagebox.showerror(
            "Error",
            "Account not found."
        )

        return

    messagebox.showinfo(
        "Account Details",

        "Account Number: " +
        account["account_number"] +

        "\n\nAccount Type: " +
        account["account_type"] +

        "\n\nCurrent Balance: Rs. " +
        str(account["balance"]) +

        "\n\nMinimum Balance: Rs. " +
        str(account["minimum_balance"])
    )

def deposit_money():

    account = find_account()

    if account is None:
        return

    amount = simpledialog.askfloat(
        "Deposit Money",
        "Enter amount to deposit:"
    )

    if amount is None:
        return

    if amount <= 0:

        messagebox.showerror(
            "Error",
            "Amount must be greater than zero."
        )

        return

    account["balance"] += amount

    transaction = {

        "account_number": account["account_number"],

        "type": "Deposit",

        "amount": amount,

        "date": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )
    }

    data["transactions"].append(transaction)

    save_data(data)

    messagebox.showinfo(
        "Success",
        "Money deposited successfully.\n\n"
        "Current Balance: Rs. " +
        str(account["balance"])
    )

def withdraw_money():

    account = find_account()

    if account is None:
        return

    amount = simpledialog.askfloat(
        "Withdraw Money",
        "Enter amount to withdraw:"
    )

    if amount is None:
        return

    if amount <= 0:

        messagebox.showerror(
            "Error",
            "Amount must be greater than zero."
        )

        return

    remaining_balance = account["balance"] - amount

    if remaining_balance < account["minimum_balance"]:

        messagebox.showerror(
            "Transaction Failed",

            "Minimum balance must be maintained.\n\n"
            "Minimum Balance: Rs. " +
            str(account["minimum_balance"]) +

            "\nCurrent Balance: Rs. " +
            str(account["balance"])
        )

        return

    account["balance"] = remaining_balance

    transaction = {

        "account_number": account["account_number"],

        "type": "Withdrawal",

        "amount": amount,

        "date": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )
    }

    data["transactions"].append(transaction)

    save_data(data)

    messagebox.showinfo(
        "Success",
        "Money withdrawn successfully.\n\n"
        "Current Balance: Rs. " +
        str(account["balance"])
    )

def transaction_history():

    account = find_account()

    if account is None:
        return

    history_window = tk.Toplevel(root)

    history_window.title(
        "Transaction History"
    )

    history_window.geometry(
        "700x500"
    )

    tk.Label(
        history_window,
        text="Transaction History",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    text_box = tk.Text(
        history_window,
        width=80,
        height=22
    )

    text_box.pack(
        padx=20,
        pady=10
    )

    found = False

    for transaction in data["transactions"]:

        if (
            transaction["account_number"]
            == account["account_number"]
        ):

            found = True

            text_box.insert(
                tk.END,
                "Type: " +
                transaction["type"] +

                "\nAmount: Rs. " +
                str(transaction["amount"]) +

                "\nDate: " +
                transaction["date"] +

                "\n" +
                "-" * 60 +
                "\n"
            )

    if not found:

        text_box.insert(
            tk.END,
            "No transactions found."
        )

    text_box.config(
        state="disabled"
    )

def card_section():

    card_window = tk.Toplevel(root)

    card_window.title(
        "Debit / Credit Card"
    )

    card_window.geometry(
        "500x500"
    )

    tk.Label(
        card_window,
        text="Debit / Credit Card",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    def apply_debit():

        create_card("Debit Card")

    def apply_credit():

        create_card("Credit Card")

    tk.Button(
        card_window,
        text="Apply for Debit Card",
        width=30,
        height=2,
        command=apply_debit
    ).pack(pady=10)

    tk.Button(
        card_window,
        text="Apply for Credit Card",
        width=30,
        height=2,
        command=apply_credit
    ).pack(pady=10)

    tk.Button(
        card_window,
        text="View My Cards",
        width=30,
        height=2,
        command=view_cards
    ).pack(pady=10)

    tk.Button(
        card_window,
        text="Block Card",
        width=30,
        height=2,
        command=block_card
    ).pack(pady=10)


def create_card(card_type):

    for card in data["cards"]:

        if (
            card["customer_id"] == current_customer_id
            and card["card_type"] == card_type
            and card["status"] == "Active"
        ):

            messagebox.showwarning(
                "Card Already Exists",
                "You already have an active " +
                card_type
            )

            return

    card_number = generate_card_number()

    cvv = str(
        random.randint(100, 999)
    )

    card = {

        "customer_id": current_customer_id,

        "card_type": card_type,

        "card_number": card_number,

        "cvv": cvv,

        "expiry": "09/31",

        "status": "Active"
    }

    if card_type == "Credit Card":

        card["credit_limit"] = 50000

        card["available_limit"] = 50000

    else:

        card["credit_limit"] = 0

        card["available_limit"] = 0

    data["cards"].append(card)

    save_data(data)

    messagebox.showinfo(
        "Card Created",

        card_type +
        " created successfully!\n\n"

        "Card Number: " +
        card_number +

        "\nCVV: " +
        cvv +

        "\nExpiry: 09/31"
    )

def view_cards():

    card_window = tk.Toplevel(root)

    card_window.title(
        "My Cards"
    )

    card_window.geometry(
        "700x500"
    )

    tk.Label(
        card_window,
        text="My Cards",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    text_box = tk.Text(
        card_window,
        width=80,
        height=22
    )

    text_box.pack(
        padx=20,
        pady=10
    )

    found = False

    for card in data["cards"]:

        if card["customer_id"] == current_customer_id:

            found = True

            text_box.insert(
                tk.END,

                "Card Type: " +
                card["card_type"] +

                "\nCard Number: " +
                card["card_number"] +

                "\nCVV: " +
                card["cvv"] +

                "\nExpiry: " +
                card["expiry"] +

                "\nStatus: " +
                card["status"]
            )

            if card["card_type"] == "Credit Card":

                text_box.insert(
                    tk.END,

                    "\nCredit Limit: Rs. " +
                    str(card["credit_limit"]) +

                    "\nAvailable Limit: Rs. " +
                    str(card["available_limit"])
                )

            text_box.insert(
                tk.END,
                "\n" + "-" * 60 + "\n"
            )

    if not found:

        text_box.insert(
            tk.END,
            "No cards found."
        )

    text_box.config(
        state="disabled"
    )


def block_card():

    card_number = simpledialog.askstring(
        "Block Card",
        "Enter card number:"
    )

    if not card_number:
        return

    for card in data["cards"]:

        if (
            card["customer_id"] == current_customer_id
            and card["card_number"] == card_number
        ):

            if card["status"] == "Blocked":

                messagebox.showwarning(
                    "Already Blocked",
                    "Card is already blocked."
                )

                return

            card["status"] = "Blocked"

            save_data(data)

            messagebox.showinfo(
                "Success",
                "Card blocked successfully."
            )

            return

    messagebox.showerror(
        "Error",
        "Card not found."
    )


def loan_section():

    loan_window = tk.Toplevel(root)

    loan_window.title(
        "Loan Section"
    )

    loan_window.geometry(
        "550x650"
    )

    tk.Label(
        loan_window,
        text="Loan Section",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    loan_types = [

        "Personal Loan",
        "Home Loan",
        "Education Loan",
        "Car Loan",
        "Business Loan",
        "Gold Loan"
    ]

    for loan_type in loan_types:

        tk.Button(
            loan_window,
            text=loan_type,
            width=35,
            height=2,
            command=lambda x=loan_type:
            apply_loan(x)
        ).pack(pady=5)

    tk.Button(
        loan_window,
        text="View My Loans",
        width=35,
        height=2,
        command=view_loans
    ).pack(pady=15)


def apply_loan(loan_type):

    loan_conditions = {

        "Personal Loan": {
            "min_age": 21,
            "min_income": 20000,
            "max_amount": 500000,
            "interest": 10
        },

        "Home Loan": {
            "min_age": 21,
            "min_income": 30000,
            "max_amount": 5000000,
            "interest": 8
        },

        "Education Loan": {
            "min_age": 18,
            "min_income": 15000,
            "max_amount": 1000000,
            "interest": 7
        },

        "Car Loan": {
            "min_age": 21,
            "min_income": 25000,
            "max_amount": 1500000,
            "interest": 9
        },

        "Business Loan": {
            "min_age": 21,
            "min_income": 30000,
            "max_amount": 3000000,
            "interest": 11
        },

        "Gold Loan": {
            "min_age": 18,
            "min_income": 10000,
            "max_amount": 500000,
            "interest": 9
        }
    }

    condition = loan_conditions[loan_type]

    age = simpledialog.askinteger(
        loan_type,
        "Enter your age:"
    )

    if age is None:
        return

    income = simpledialog.askfloat(
        loan_type,
        "Enter monthly income:"
    )

    if income is None:
        return

    if age < condition["min_age"]:

        messagebox.showerror(
            "Loan Rejected",
            "Minimum age required: " +
            str(condition["min_age"])
        )

        return

    if income < condition["min_income"]:

        messagebox.showerror(
            "Loan Rejected",
            "Minimum monthly income required: Rs. " +
            str(condition["min_income"])
        )

        return

    account = find_account()

    if account is None:
        return

    if account["balance"] < account["minimum_balance"]:

        messagebox.showerror(
            "Loan Rejected",
            "You must maintain the minimum account balance."
        )

        return

    amount = simpledialog.askfloat(
        loan_type,
        "Enter loan amount:"
    )

    if amount is None:
        return

    duration = simpledialog.askinteger(
        loan_type,
        "Enter duration in months:"
    )

    if duration is None:
        return

    if amount <= 0:

        messagebox.showerror(
            "Error",
            "Loan amount must be greater than zero."
        )

        return

    if amount > condition["max_amount"]:

        messagebox.showerror(
            "Loan Rejected",
            "Maximum loan amount is Rs. " +
            str(condition["max_amount"])
        )

        return

    if duration <= 0:

        messagebox.showerror(
            "Error",
            "Duration must be greater than zero."
        )

        return



    for loan in data["loans"]:

        if (
            loan["customer_id"] == current_customer_id
            and loan["loan_type"] == loan_type
            and loan["status"] in ["Pending", "Active"]
        ):

            messagebox.showwarning(
                "Loan Exists",
                "You already have an active or pending " +
                loan_type
            )

            return



    interest_rate = condition["interest"]

    monthly_rate = interest_rate / (12 * 100)

    emi = (

        amount
        * monthly_rate
        * (1 + monthly_rate) ** duration

    ) / (

        (1 + monthly_rate) ** duration - 1
    )

    result = (

        "Loan Type: " + loan_type +

        "\n\nLoan Amount: Rs. " +
        str(amount) +

        "\n\nInterest Rate: " +
        str(interest_rate) + "%" +

        "\n\nDuration: " +
        str(duration) + " months" +

        "\n\nMonthly EMI: Rs. " +
        str(round(emi, 2))
    )

    confirm = messagebox.askyesno(
        "Confirm Loan Application",
        result +
        "\n\nDo you want to apply?"
    )

    if not confirm:
        return

    loan_id = generate_loan_id()

    loan = {

        "loan_id": loan_id,

        "customer_id": current_customer_id,

        "loan_type": loan_type,

        "amount": amount,

        "interest_rate": interest_rate,

        "duration": duration,

        "emi": round(emi, 2),

        "status": "Pending",

        "date": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )
    }

    data["loans"].append(loan)

    save_data(data)

    messagebox.showinfo(
        "Loan Application",
        "Loan application submitted successfully!\n\n"
        "Loan ID: " + loan_id +
        "\nStatus: Pending"
    )


def view_loans():

    loan_window = tk.Toplevel(root)

    loan_window.title(
        "My Loans"
    )

    loan_window.geometry(
        "750x550"
    )

    tk.Label(
        loan_window,
        text="My Loans",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    text_box = tk.Text(
        loan_window,
        width=85,
        height=25
    )

    text_box.pack(
        padx=20,
        pady=10
    )

    found = False

    for loan in data["loans"]:

        if loan["customer_id"] == current_customer_id:

            found = True

            text_box.insert(
                tk.END,

                "Loan ID: " +
                loan["loan_id"] +

                "\nLoan Type: " +
                loan["loan_type"] +

                "\nAmount: Rs. " +
                str(loan["amount"]) +

                "\nInterest Rate: " +
                str(loan["interest_rate"]) + "%" +

                "\nDuration: " +
                str(loan["duration"]) +
                " months" +

                "\nMonthly EMI: Rs. " +
                str(loan["emi"]) +

                "\nStatus: " +
                loan["status"] +

                "\nDate: " +
                loan["date"] +

                "\n" + "-" * 65 +
                "\n"
            )

    if not found:

        text_box.insert(
            tk.END,
            "No loans found."
        )

    text_box.config(
        state="disabled"
    )



def customer_service():

    service_window = tk.Toplevel(root)

    service_window.title(
        "Customer Service"
    )

    service_window.geometry(
        "550x550"
    )

    tk.Label(
        service_window,
        text="Customer Service",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Button(
        service_window,
        text="Register Complaint",
        width=35,
        height=2,
        command=register_complaint
    ).pack(pady=8)

    tk.Button(
        service_window,
        text="View My Complaints",
        width=35,
        height=2,
        command=view_complaints
    ).pack(pady=8)

    tk.Button(
        service_window,
        text="Change Password",
        width=35,
        height=2,
        command=change_password
    ).pack(pady=8)

    tk.Button(
        service_window,
        text="Change PIN",
        width=35,
        height=2,
        command=change_pin
    ).pack(pady=8)

    tk.Button(
        service_window,
        text="Bank Number & Bank Details",
        width=35,
        height=2,
        command=bank_details
    ).pack(pady=8)

def register_complaint():

    complaint_window = tk.Toplevel(root)

    complaint_window.title(
        "Register Complaint"
    )

    complaint_window.geometry(
        "500x450"
    )

    tk.Label(
        complaint_window,
        text="Register Complaint",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(
        complaint_window,
        text="Complaint Type:"
    ).pack()

    complaint_type = tk.StringVar()

    complaint_type.set(
        "Account Issue"
    )

    options = [

        "Account Issue",
        "Card Issue",
        "Loan Issue",
        "Transaction Issue",
        "Other"
    ]

    dropdown = tk.OptionMenu(
        complaint_window,
        complaint_type,
        *options
    )

    dropdown.pack(pady=10)

    tk.Label(
        complaint_window,
        text="Description:"
    ).pack()

    description = tk.Text(
        complaint_window,
        width=45,
        height=8
    )

    description.pack(pady=10)

    def submit():

        text = description.get(
            "1.0",
            tk.END
        ).strip()

        if not text:

            messagebox.showerror(
                "Error",
                "Please enter complaint description."
            )

            return

        request_id = generate_request_id()

        request = {

            "request_id": request_id,

            "customer_id": current_customer_id,

            "type": complaint_type.get(),

            "description": text,

            "status": "Pending",

            "date": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        }

        data["service_requests"].append(request)

        save_data(data)

        messagebox.showinfo(
            "Complaint Registered",
            "Complaint registered successfully!\n\n"
            "Request ID: " + request_id
        )

        complaint_window.destroy()

    tk.Button(
        complaint_window,
        text="Submit Complaint",
        width=25,
        height=2,
        command=submit
    ).pack(pady=10)


def view_complaints():

    complaint_window = tk.Toplevel(root)

    complaint_window.title(
        "My Complaints"
    )

    complaint_window.geometry(
        "750x500"
    )

    tk.Label(
        complaint_window,
        text="My Complaints",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    text_box = tk.Text(
        complaint_window,
        width=85,
        height=22
    )

    text_box.pack(
        padx=20,
        pady=10
    )

    found = False

    for request in data["service_requests"]:

        if request["customer_id"] == current_customer_id:

            found = True

            text_box.insert(
                tk.END,

                "Request ID: " +
                request["request_id"] +

                "\nType: " +
                request["type"] +

                "\nDescription: " +
                request["description"] +

                "\nStatus: " +
                request["status"] +

                "\nDate: " +
                request["date"] +

                "\n" + "-" * 65 +
                "\n"
            )

    if not found:

        text_box.insert(
            tk.END,
            "No complaints found."
        )

    text_box.config(
        state="disabled"
    )

def change_password():

    customer = find_customer()

    if customer is None:
        return

    old_password = simpledialog.askstring(
        "Change Password",
        "Enter current password:",
        show="*"
    )

    if old_password is None:
        return

    if old_password != customer["password"]:

        messagebox.showerror(
            "Error",
            "Incorrect current password."
        )

        return

    new_password = simpledialog.askstring(
        "Change Password",
        "Enter new password:",
        show="*"
    )

    if new_password is None:
        return

    if len(new_password) < 4:

        messagebox.showerror(
            "Error",
            "Password must contain at least 4 characters."
        )

        return

    confirm_password = simpledialog.askstring(
        "Change Password",
        "Confirm new password:",
        show="*"
    )

    if new_password != confirm_password:

        messagebox.showerror(
            "Error",
            "Passwords do not match."
        )

        return

    customer["password"] = new_password

    save_data(data)

    messagebox.showinfo(
        "Success",
        "Password changed successfully."
    )



def change_pin():

    customer = find_customer()

    if customer is None:
        return

    old_pin = simpledialog.askstring(
        "Change PIN",
        "Enter current PIN:",
        show="*"
    )

    if old_pin is None:
        return

    if old_pin != customer["pin"]:

        messagebox.showerror(
            "Error",
            "Incorrect current PIN."
        )

        return

    new_pin = simpledialog.askstring(
        "Change PIN",
        "Enter new 4-digit PIN:",
        show="*"
    )

    if new_pin is None:
        return

    if len(new_pin) != 4 or not new_pin.isdigit():

        messagebox.showerror(
            "Error",
            "PIN must contain exactly 4 digits."
        )

        return

    confirm_pin = simpledialog.askstring(
        "Change PIN",
        "Confirm new PIN:",
        show="*"
    )

    if new_pin != confirm_pin:

        messagebox.showerror(
            "Error",
            "PINs do not match."
        )

        return

    customer["pin"] = new_pin

    save_data(data)

    messagebox.showinfo(
        "Success",
        "PIN changed successfully."
    )


def bank_details():

    customer = find_customer()

    account = find_account()

    if customer is None or account is None:
        return

    messagebox.showinfo(

        "Bank Details",

        "ABC BANK\n"
        "============================\n\n"

        "Bank Name: ABC Bank\n"

        "Bank Number: 1234567890\n"

        "Branch: Pune Main Branch\n"

        "IFSC Code: ABCD0001234\n\n"

        "Customer Name: " +
        customer["name"] +

        "\nPhone Number: " +
        customer["phone"] +

        "\nEmail: " +
        customer["email"] +

        "\nAddress: " +
        customer["address"] +

        "\n\nAccount Number: " +
        account["account_number"] +

        "\nAccount Type: " +
        account["account_type"]
    )


def logout():

    global current_customer_id

    answer = messagebox.askyesno(
        "Logout",
        "Do you want to logout?"
    )

    if answer:

        current_customer_id = None

        home_page()


home_page()

root.mainloop()


