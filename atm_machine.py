from logo import logo
import random
import json

print(logo)
taken_usernames = []


def main_menu():
    """A function to display the Main Menu"""
    print("\n\tMAIN MENU: ")
    print("\t\t1. Create Account")
    print("\t\t2. Checkin")
    print("\t\t3. Exit")

    try:
        choice = int(input("\nChoose from the Main Menu: "))
        if choice in (1, 2, 3):
            return choice
        else:
            print("Invalid Choice.Choose from the Provided Menu.")
            main_menu()
    except ValueError:
        print("Invalid Literal Entered.")
        main_menu()


def sub_menu():
    """A function to display the Sub-Menu"""
    print("\n\t SUB MENU: ")
    print("\t\t 1. Account Detail")
    print("\t\t 2. Deposit")
    print("\t\t 3. Withdraw")
    print("\t\t 4. Update Pin")
    print("\t\t 5. Check Statement")
    print("\t\t 6. Logout")

    try:
        choice = int(input("\nChoose from the Sub-Menu: "))
        if choice in (1, 2, 3, 4, 5, 6):
            return choice
        else:
            print("Invalid Choice.Choose from the Provided Menu.")
            sub_menu()
    except ValueError:
        print("Invalid Literal Entered.")
        sub_menu()


def collect_data():
    try:
        with open("users.json", "r") as data_file:
            my_data = json.load(data_file)
            return my_data
    except FileNotFoundError:
        return {}


def create_account():
    """A function to Create a New Account"""

    input_name = input("Enter Your Name: ")
    amount = int(input("Enter Amount to Deposit (Should be More than 50): "))
    while amount < 50:
        amount = int(input("Enter more amount to deposit: "))
    balance_amount = amount

    code = input("Enter a 4-digit Pin_Code: ")
    while len(code) != 4 or not code.isdigit():
        code = input("Enter Your Pin_Code Again: ")

    print("\nAccount Created Successfully.")
    return input_name, amount, balance_amount, code


def auto_generate_info(user, d_amount, pin, total_balance):
    your_id = [f"{random.randint(0, 9)}" for _ in range(10)]
    user_id = "".join(your_id)

    digits = [f"{random.randint(0, 9)}" for _ in range(4)]
    user_name = user + "_" + "".join(digits)

    if user_name in taken_usernames:
        digits = [f"{random.randint(0, 9)}" for _ in range(4)]
        user_name = user + "_" + "".join(digits)
    taken_usernames.append(user_name)

    status = "ACTIVE"
    currency = "PKR"

    print(f"\nYour Information:\n Username: {user_name}\n Account Number: {user_id}")

    return {
        user_name:
            {
                "User_ID": user_id,
                "Name": user,
                "Currency": currency,
                "Pin-Code": pin,
                "Status": status,
                "Account Details:": {
                    "Balance_Amount": total_balance,
                    "Currency": "PKR",
                    "Statement": [{'Deposited of PKR': d_amount}]
                }
            }
    }


def write_to_file(data):
    try:
        with open("users.json", "r") as my_file:
            file_data = json.load(my_file)
    except FileNotFoundError:
        with open("users.json", "w") as file:
            json.dump(data, file, indent=4)
    else:
        file_data.update(data)
        with open("users.json", "w") as my_file:
            json.dump(file_data, my_file, indent=4)


def verify_username(user_name):
    """A function to check if the user exists."""
    try:
        value = input("Enter your Username: ")
        if value == user_name:
            return True
        else:
            return False
    except ValueError:
        print("Invalid Input.")


def verify_pin(data, user):
    """A function to check the PIN code"""
    for _ in range(3):
        code = input("Enter Your Pin-Code: ")
        if data[user]["Pin-Code"] == code:
            print("You can Proceed. ")
            return True
        else:
            print("Incorrect PIN. Please try again.")
    print("Incorrect PIN entered three times. User is now BLOCKED.")
    return False


def checkin(data):
    result = ""
    try:
        current_username = input("Enter Username: ")
    except ValueError:
        print("Invalid input.")
    else:
        if current_username in data:
            if verify_pin(data, current_username):
                result = True
            else:
                data[f"{current_username}"]["Status"] = "BLOCKED"
                write_to_file(data)
        else:
            print("No such User Exists.")

        return current_username, result


def deposit_amount(data, user):
    try:
        amount = int(input("Enter amount to Deposit(More than 50): "))
        while amount < 50:
            amount = int(input("Again Enter amount to Deposit:  "))

        bal = data[user]["Account Details:"]["Balance_Amount"]
        new_balance = amount + bal

        data[user]["Account Details:"]["Balance_Amount"] = new_balance
        print(f"New Balance: {new_balance}")

        description = {"Deposited of PKR": amount}
        data[user]["Account Details:"]["Statement"].append(description)
        write_to_file(data)
        print("Balance Updated Successfully.")
    except ValueError:
        print("Invalid input. Please enter a valid amount.")


def withdraw_amount(data, user):
    """A function to withdraw money from the account"""
    if data[user]["Status"] == "BLOCKED":
        print("User is Blocked. Can not Withdraw Amount. ")
    else:
        total_balance = data[user]["Account Details:"]["Balance_Amount"]
        try:
            amount = int(input("Enter amount to withdraw: "))
            tax = (amount * 1) / 100
            total_amount = amount + tax
            if total_amount <= total_balance:
                total_balance -= total_amount
                print(f"New Balance: {total_balance}")
                data[user]["Account Details:"]["Balance_Amount"] = total_balance

                description = {"Withdrawal of PKR": amount}
                data[user]["Account Details:"]["Statement"].append(description)
                write_to_file(data)
                print("Transaction Successful.")

            else:
                print("Insufficient Balance. ")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")


def update_pin(data, user):
    """A function to update user's current pin-code."""
    try:
        pin = input("Enter Your Current Pin-Code: ")
        if pin == data[user]["Pin-Code"]:
            new_pin = input("Enter Your New Pin-Code: ")
            data[user]["Pin-Code"] = new_pin
            write_to_file(data)
            print("Pin-Code Updated Successfully.")
        else:
            print("Incorrect Pin Entered. ")
    except ValueError:
        print("Enter a valid pin-code")


def check_statement(data, user):
    user_name = user[0:-5]
    if len(data) > 0:
        with open(f"statement_{user_name}.txt", "w") as file:
            statements = data[user]["Account Details:"]["Statement"]
            file.write(f"\nUsername: {user}\n {json.dumps(statements, indent=2)}")
            print(f"Please Check the 'statement_{user_name}.txt' file.")
    else:
        print("Sorry. Data Unavailable.")


machine_on = True

while machine_on:
    # Display Main_Menu
    user_choice = main_menu()

    # 1. Handling Create Account Module
    if user_choice == 1:
        name, deposit, balance, pin_code = create_account()
        data_generated = auto_generate_info(name, deposit, pin_code, balance)
        write_to_file(data_generated)

    # 2. Handling Checkin Module
    elif user_choice == 2:
        available_data = collect_data()
        if len(available_data) > 0:
            current_user, condition = checkin(available_data)

            if condition:
                # Handling Sub-Menu
                while True:
                    # Display Sub-Menu
                    sub_choice = sub_menu()

                    # 2.1 Handling Account Detail module
                    if sub_choice == 1:
                        account_details = available_data[f"{current_user}"]
                        print(f" Account Details:\n{json.dumps(account_details, indent=4)}")

                    # 2.2 Handling Deposit Module
                    elif sub_choice == 2:
                        deposit_amount(available_data, current_user)

                    # 2.3 Handling Withdraw Module
                    elif sub_choice == 3:
                        withdraw_amount(available_data, current_user)

                    # 2.4 Handling Update Pin Module
                    elif sub_choice == 4:
                        update_pin(available_data, current_user)

                    # 2.5 Handling Check Statement Module
                    elif sub_choice == 5:
                        check_statement(available_data, current_user)

                    # 2.6 Handling Logout Module
                    elif sub_choice == 6:
                        print("Logging Out...")
                        break
            else:
                continue
        else:
            print("Create an Account First.")

    # 3. Handling Exit Module
    elif user_choice == 3:
        print("GoodBye...")
        machine_on = False
