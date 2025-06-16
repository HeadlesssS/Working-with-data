from datetime import datetime

new_vat_total = 0

def generate_invoice(total, location, employee_name,  file_no=None, print_final_total=True):
    global new_vat_total
    now = datetime.now()

    # If file_no is not provided, create a new invoice file
    if file_no is None:
        file_no = 1
        while True:
            try:
                with open(f"filelog{file_no}.txt", "x") as file:
                    file.write(f"Invoice no : {file_no}                                  time:{now.hour}:{now.minute}\n")
                    file.write(f"                                                date:{now.year}/{now.month}/{now.day}\n")
                    file.write("\n--------------------|------------------------------|--------\n")
                    file.write("**------------------*-----------BRJ FURNITURE------*------**\n")
                    file.write("--------------------|------------------------------|--------\n")
                    file.write("Item                | Details                      | Value\n")
                    file.write("--------------------|------------------------------|--------\n\n")
                    break
            except FileExistsError:
                file_no += 1

    # Read the existing file to find previous cumulative totals
    previous_vat_total = 0
    if file_no is not None:
        try:
            with open(f"filelog{file_no}.txt", "r") as file:
                for line in file:
                    if "Final Total after VAT" in line:
                        previous_vat_total += float(line.strip().split("$")[-1])
        except FileNotFoundError:
            pass

    # Calculate the current transaction's VAT-inclusive total
    if location in ["no", "n"]:
        shipping_cost = 0.05 * total
        ship_total = total + shipping_cost
        vat_total = ship_total * 1.13
    else:
        ship_total = total
        vat_total = ship_total * 1.13

    # Write the transaction details
    with open(f"filelog{file_no}.txt", "a") as file:
        if not print_final_total:
            # Write details in a simple tabular format
            file.write(f"Total               |                               | {total}\n")
            if location in ["no", "n"]:
                file.write(f"Shipping Cost       | 5% shipping cost             | ${shipping_cost:.2f}\n")
                file.write(f"Price after Shipping|                              | ${ship_total:.2f}\n")
                print(f"Shipping Cost       | 5% shipping cost             | ${shipping_cost:.2f}\n")
                print(f"Price after Shipping|                              | ${ship_total:.2f}\n")
            else:
                file.write(f"Shipping            | Free within Nepal            | -\n")
                print(f"Shipping    | Free within Nepal")
                
            file.write(f"Total with VAT     | 13% VAT                      | ${vat_total:.2f}\n")
            new_vat_total += vat_total
            

        if print_final_total:
            
            # Calculate and format the final cumulative total
            final_total = new_vat_total
            file.write("--------------------|------------------------------|--------\n")
            file.write(f"Final Total after VAT:{final_total:.2f}\n")
            file.write("--------------------|------------------------------|--------\n\n")
            
            
            file.write(f"Transaction made by employee: {employee_name}")
            file.write(f"\n{'-'*50}\n")

    return file_no
