# ABC Bank Management System

A simple **Bank Management System** built with **Python, Tkinter, and JSON**. The application provides a desktop GUI for customer registration, login, account management, transactions, cards, loans, and customer service requests.

## Features

- Customer registration and login
- Savings account creation and account details
- Deposit and withdrawal operations
- Transaction history
- Card creation, viewing, and blocking
- Loan application and loan status viewing
- Customer service / complaint registration
- Password and PIN change
- Local JSON-based data storage

## Technologies Used

- Python 3
- Tkinter
- JSON
- File handling

## Project Structure

```text
abc-bank-management-system/
├── bank.py
├── bank_data.json
├── README.md
└── .gitignore
```

## Requirements

- Python 3.x
- Tkinter (normally included with standard Python installations)

No third-party Python packages are required.

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/abc-bank-management-system.git
```

2. Open the project folder:

```bash
cd abc-bank-management-system
```

3. Run the application:

```bash
python bank.py
```

The application will create/update `bank_data.json` locally as data is entered.

## Important Note

This project is intended for **educational/demo purposes**. It is not suitable for real banking or production use. Passwords/PINs and financial records are stored locally in JSON and are not protected with production-grade authentication or encryption.

The repository starts with an empty `bank_data.json` and does not contain real customer credentials.

## Author

Divya Nagpurne
