import datetime

def generate_receipt():
    print("=== Payment Receipt Generator ===")
    
    # Collect input
    customer_name = input("Enter customer name: ")
    items = []
    total_amount = 0.0

    while True:
        item_name = input("Enter item name (or type 'done' to finish): ")
        if item_name.lower() == 'done':
            break
        try:
            item_price = float(input(f"Enter price for '{item_name}': "))
            items.append((item_name, item_price))
            total_amount += item_price
        except ValueError:
            print("Invalid input. Please enter a valid number for price.")

    # Date and time
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Receipt formatting
    receipt_lines = [
        "=======================================",
        "           PAYMENT RECEIPT             ",
        "=======================================",
        f"Date: {date_time}",
        f"Customer: {customer_name}",
        "---------------------------------------",
        "Items:"
    ]

    for name, price in items:
        receipt_lines.append(f"  - {name}: ${price:.2f}")

    receipt_lines.append("---------------------------------------")
    receipt_lines.append(f"Total Amount: ${total_amount:.2f}")
    receipt_lines.append("=======================================")
    receipt_text = "\n".join(receipt_lines)

    print("\n" + receipt_text)

    # Optionally save to file
    save = input("Do you want to save the receipt to a file? (yes/no): ").strip().lower()
    if save == 'yes':
        filename = f"receipt_{now.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as file:
            file.write(receipt_text)
        print(f"Receipt saved to '{filename}'")

if __name__ == "__main__":
    generate_receipt()
