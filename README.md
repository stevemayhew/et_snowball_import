# et_snowball_import
Python convert E*Trade Transactions to Snowball Analytics

# Steps
1. Go to the ETrade [account transacactions page]([url](https://us.etrade.com/e/t/accounts/txnhistory))
2. Select the download icon (next to help and print)
3. Download one year at a time (max ETrade allows) as far back as it will let you
4. Concatenate the downloaded files and remove all but the first CSV header line
5. Run this script

```
python3 translate_csv.py etrade_transactions.csv 1>snowball_custom.csv
```

Script prints the transaction lines it ignores (may be worth noting for later cleanup)

Upload to Snowball, then connect to ETrade with Yodlee


