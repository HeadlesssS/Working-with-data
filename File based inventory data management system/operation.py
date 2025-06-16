from write import generate_invoice
from datetime import datetime

id = [1, 2, 3, 4, 5, 6]

def read_file():
    """Read the contents of 'info.txt'."""
    try:
        with open("info.txt", "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print("Error: 'info.txt' not found.")
        return []

def write_file(lines):
    """Write the updated lines back to 'info.txt'."""
    with open("info.txt", "w") as file:
        file.writelines(lines)

def buy(existing_file_no=None, employee_name=None, location=None):
    all_lines = read_file()
    if not all_lines:
        return 0

    print("Buying option selected.")

    if employee_name is None:
        location = input("Are you from Nepal? (yes or no): ").strip().lower()
        employee_name = input("Enter your name: ").strip()

    while True:
        id_input = input("Enter the item id: ")
        try:
            id_input = int(id_input)
            if id_input in id:
                try:
                    while True:
                        quantity = int(input("Enter the quantity of the products you want to buy: "))
                        if quantity>0:
                            break
                    transaction_total = 0 

                    for i in range(3, len(all_lines)-1):
                        line = all_lines[i].strip().split("|")
                        if len(line) == 5:
                            SN, name, item, qty, price = line
                            price = float(price.replace("$", ""))
                            if id_input == int(SN):
                                qty = int(qty) + quantity
                                all_lines[i] = f"{SN}| {name}| {item}| {qty}| ${price:.2f}\n"
                                transaction_total += quantity * price
                                
                                write_file(all_lines)
                                print(f"You bought {quantity} {item}")
                                print(f"the cost is {transaction_total}")

                                # Generate invoice for the current transaction
                                if existing_file_no is None:
                                    existing_file_no = generate_invoice(transaction_total, location, employee_name, file_no=None, print_final_total=False)
                                else:
                                    generate_invoice(transaction_total, location, employee_name, file_no=existing_file_no, print_final_total=False)

                                again = input("Do you want to buy more? (yes or no): ").strip().lower()
                                if again == "yes":
                                    return buy(existing_file_no=existing_file_no, employee_name=employee_name, location=location)
                                if again == "no":
                                    generate_invoice(transaction_total, location, employee_name, file_no=existing_file_no, print_final_total=True)
                                    return transaction_total
                except ValueError:
                    print("Quantity should be a number.")
            else:
                print("Item not found, try again.")
        except ValueError:
            print("Enter a valid number.")
            



def sell(existing_file_no=None, employee_name=None, location=None):
    all_lines = read_file()
    if not all_lines:
        return 0

    print("Selling option selected.")

    if employee_name is None:
        location = input("Are you from Nepal? (yes or no): ").strip().lower()
        employee_name = input("Enter your name: ").strip()

    while True:
        id_input = input("Enter the item id: ")
        try:
            id_input = int(id_input)
            if id_input in id:
                try:
                    quantity = int(input("Enter the quantity of the products you want to sell: "))

                    transaction_total = 0  # Use a separate total for the current transaction

                    for i in range(3, len(all_lines)-1):
                        line = all_lines[i].strip().split("|")
                        if len(line) == 5:
                            SN, name, item, qty, price = line
                            price = float(price.replace("$", ""))
                            if id_input == int(SN):
                                qty = int(qty)
                                if qty >= quantity:
                                    qty -= quantity
                                    all_lines[i] = f"{SN}| {name}| {item}| {qty}| ${price:.2f}\n"
                                    transaction_total += quantity * price
                                    write_file(all_lines)
                                    print(f"You sold {quantity} {item}")
                                    print(f"the earnings are {transaction_total}")
                                    # Generate invoice for the current transaction
                                    if existing_file_no is None:
                                        existing_file_no = generate_invoice(transaction_total, location, employee_name, file_no=None, print_final_total=False)
                                    else:
                                        generate_invoice(transaction_total, location, employee_name,  file_no=existing_file_no, print_final_total=False)

                                    again = input("Do you want to sell more? (yes or no): ").strip().lower()
                                    if again == "yes":
                                        return sell(existing_file_no=existing_file_no, employee_name=employee_name, location=location)
                                    if again == "no":
                                        generate_invoice(transaction_total, location, employee_name,  file_no=existing_file_no, print_final_total=True)
                                        return transaction_total
                                
                                else:
                                    print("Insufficient quantity in stock.")
                                    return 0
                            else:
                                print("enter valid number")
                except ValueError:
                    print("Quantity should be a number.")
            else:
                print("Product not found, try again.")
        except ValueError:
            print("Enter a valid number.")
