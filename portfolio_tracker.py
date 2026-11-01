"""Stock portfolio tracker for the CodeAlpha internship task."""

import csv
from pathlib import Path

STOCK_PRICES = {"AAPL": 180.0, "TSLA": 250.0, "MSFT": 420.0, "AMZN": 190.0, "GOOGL": 175.0}


def calculate_portfolio(holdings, prices=STOCK_PRICES):
    """Return per-stock values and the total for {symbol: quantity}."""
    values = {}
    for symbol, quantity in holdings.items():
        symbol = symbol.upper()
        if symbol not in prices:
            raise ValueError(f"Unsupported stock symbol: {symbol}")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        values[symbol] = round(quantity * prices[symbol], 2)
    return values, round(sum(values.values()), 2)


def save_csv(holdings, path, prices=STOCK_PRICES):
    values, total = calculate_portfolio(holdings, prices)
    with Path(path).open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Symbol", "Quantity", "Price", "Value"])
        for symbol, value in values.items():
            writer.writerow([symbol, holdings[symbol], prices[symbol], value])
        writer.writerow(["TOTAL", "", "", total])
    return total


def interactive():
    holdings = {}
    print("Available stocks:", ", ".join(STOCK_PRICES))
    print("Enter 'done' when finished.")
    while True:
        symbol = input("Stock symbol: ").strip().upper()
        if symbol == "DONE":
            break
        if symbol not in STOCK_PRICES:
            print("Unknown symbol. Choose from the available stocks.")
            continue
        try:
            quantity = float(input("Quantity: "))
            if quantity < 0:
                raise ValueError
        except ValueError:
            print("Enter a non-negative number for quantity.")
            continue
        holdings[symbol] = holdings.get(symbol, 0) + quantity
    values, total = calculate_portfolio(holdings)
    for symbol, value in values.items():
        print(f"{symbol}: ${value:,.2f}")
    print(f"Total investment: ${total:,.2f}")
    if input("Save a CSV report? (y/n): ").strip().lower() == "y":
        save_csv(holdings, "portfolio_report.csv")
        print("Saved portfolio_report.csv")


if __name__ == "__main__":
    interactive()
