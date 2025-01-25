import csv
from datetime import datetime
import sys
import sys

def translate_csv():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r') as infile:
            input_data = infile.read().strip().splitlines()
    else:
        input_data = sys.stdin.read().strip().splitlines()

    reader = csv.DictReader(input_data)
    fieldnames = [
        "Event", "Date", "Symbol", "Price", "Quantity", "Currency", "FeeTax", "Exchange", "FeeCurrency", "DoNotAdjustCash", "Note"
    ]

    ignored_transaction_types = [
        "Adjustment", "Sold Short"
    ]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    row_num = 1;
    for row in reader:
        event = "Unknown"
        # Retrieve TransactionType safely, skip any ignored stuff
        try:
            transaction_type = row["TransactionType"]
            if transaction_type in ignored_transaction_types:
                continue
        except KeyError:
            print(f"Missing TransactionType key in row:  {row_num} text: {row}", file=sys.stderr)
            continue
        finally:
            row_num = row_num + 1


        # Determine the Event type
        if transaction_type in ["Transfer", "Online Transfer"]:
            event = "Cash_In" if float(row["Amount"]) > 0 else "Cash_Out"
        elif transaction_type in ["Bought", "Sold"]:
            event = "Buy" if transaction_type == "Bought" else "Sell"
        elif transaction_type in ["Dividend", "Qualified Dividend"]:
            event = "Dividend"
        elif transaction_type in ["Interest", "Interest Income", "LT Cap Gain Distribution"]:
            event = "Cash_Gain"
        elif transaction_type == "Reorganization":
            event = "Spinoff"
        else:
            event = "Fee" if float(row["Commission"]) > 0 else "Unknown"

        # Parse the date
        date = datetime.strptime(row["TransactionDate"], "%m/%d/%y").strftime("%Y-%m-%d")

        # Print unknown transaction types to stderr
        if event == "Unknown":
            print(f"Unknown Transaction Type row: {row_num} text: {row}", file=sys.stderr)
        else:
            # Extract relevant fields and fill in the output format
            output_row = {
                "Event": event,
                "Date": date,
                "Symbol": row["Symbol"].strip(),
                "Price": row["Price"].strip() or 0,
                "Quantity": row["Quantity"].strip() or 0,
                "Currency": "USD",  # Assuming USD; update if needed
                "FeeTax": abs(float(row["Commission"])),
                "Exchange": "",
                "FeeCurrency": "USD",  # Assuming fee is in USD
                "DoNotAdjustCash": "",
                "Note": row["Description"].strip()
            }

            writer.writerow(output_row)


translate_csv()
