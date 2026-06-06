from decimal import Decimal, InvalidOperation

import requests

API_BASE_URL = "https://api.frankfurter.dev/v2"
REQUEST_TIMEOUT = 10
MONEY_QUANTIZER = Decimal("0.01")
RATE_QUANTIZER = Decimal("0.0001")
API_ERROR_MESSAGE = "Currency data is unavailable right now. Please try again later."


class CurrencyApiError(Exception):
    pass


def fetch_json(endpoint, params=None):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as exc:
        raise CurrencyApiError from exc


def fetch_currencies():
    data = fetch_json("/currencies")

    try:
        currencies = {
            item["iso_code"]: item["name"]
            for item in data
            if item.get("iso_code") and item.get("name")
        }
    except (AttributeError, TypeError) as exc:
        raise CurrencyApiError from exc

    if not currencies:
        raise CurrencyApiError

    return currencies


def fetch_exchange_rate(base_currency, target_currency):
    params = {
        "base": base_currency,
        "quotes": target_currency,
    }
    data = fetch_json("/rates", params=params)

    try:
        rate = Decimal(str(data[0]["rate"]))
    except (IndexError, KeyError, TypeError, InvalidOperation) as exc:
        raise CurrencyApiError from exc

    if not rate.is_finite() or rate <= 0:
        raise CurrencyApiError

    return rate


def normalize_currency(currency_text):
    return currency_text.strip().upper()


def is_supported_currency(currency_code, currencies):
    return currency_code in currencies


def parse_amount(amount_text):
    try:
        amount = Decimal(amount_text)
        if not amount.is_finite() or amount <= 0:
            return None
        return amount
    except InvalidOperation:
        return None


def convert_amount(amount, rate):
    return (amount * rate).quantize(MONEY_QUANTIZER)


def format_currency_list(currencies):
    lines = ["Supported Currencies"]
    for code in sorted(currencies.keys()):
        lines.append(f"{code} - {currencies[code]}")
    return "\n".join(lines)


def format_rate(base_currency, target_currency, rate):
    return f"1 {base_currency} = {rate:.4f} {target_currency}"


def format_conversion(amount, base_currency, converted_amount, target_currency):
    return f"{amount:.2f} {base_currency} = {converted_amount:.2f} {target_currency}"


def print_help():
    print("Welcome to the Currency Converter.")
    print("Commands:")
    print("list - show supported currencies")
    print("rate - show exchange rate")
    print("convert - convert an amount")
    print("q - quit")


def main():
    print_help()

    while True:
        command = input("Enter command: ").strip().lower()

        if command == "q":
            print("Goodbye.")
            break

        elif command == "list":
            try:
                currencies = fetch_currencies()
                print(format_currency_list(currencies))
            except CurrencyApiError:
                print(API_ERROR_MESSAGE)

        elif command == "rate":
            try:
                currencies = fetch_currencies()

                base_currency = normalize_currency(input("Enter base currency: "))
                target_currency = normalize_currency(input("Enter target currency: "))

                if not is_supported_currency(
                    base_currency, currencies
                ) or not is_supported_currency(target_currency, currencies):
                    print("Invalid currency code.")
                    continue

                rate = fetch_exchange_rate(base_currency, target_currency)
                print(format_rate(base_currency, target_currency, rate))

            except CurrencyApiError:
                print(API_ERROR_MESSAGE)

        elif command == "convert":
            try:
                currencies = fetch_currencies()

                base_currency = normalize_currency(input("Enter base currency: "))
                if not is_supported_currency(base_currency, currencies):
                    print("Invalid currency code.")
                    continue

                amount_text = input(f"Enter amount in {base_currency}: ").strip()
                amount = parse_amount(amount_text)

                if amount is None:
                    print("Amount must be a positive number.")
                    continue

                target_currency = normalize_currency(input("Enter target currency: "))
                if not is_supported_currency(target_currency, currencies):
                    print("Invalid currency code.")
                    continue

                rate = fetch_exchange_rate(base_currency, target_currency)
                converted_amount = convert_amount(amount, rate)

                print(format_conversion(amount, base_currency, converted_amount, target_currency))

            except CurrencyApiError:
                print(API_ERROR_MESSAGE)

        else:
            print("Unrecognized command.")


if __name__ == "__main__":
    main()
