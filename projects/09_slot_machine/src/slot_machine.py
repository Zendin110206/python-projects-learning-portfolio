import random as rd

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

SYMBOL_COUNT = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

SYMBOL_VALUE = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}


def deposit_money():
    while True:
        amount = input("What would you like to deposit? $")

        if not amount.isdigit():
            print("Please enter a number.")
            continue

        amount = int(amount)

        if amount > 0:
            return amount

        print("Amount must be greater than 0.")


def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES}): ")

        if not lines.isdigit():
            print("Enter a valid number of lines.")
            continue

        lines = int(lines)

        if 1 <= lines <= MAX_LINES:
            return lines

        print("Enter a valid number of lines.")


def get_bet():
    while True:
        bet = input("What would you like to bet on each line? $")

        if not bet.isdigit():
            print("Please enter a number.")
            continue

        bet = int(bet)

        if MIN_BET <= bet <= MAX_BET:
            return bet

        print(f"Amount must be between ${MIN_BET} and ${MAX_BET}.")


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []

    for symbol, count in symbols.items():
        for _ in range(count):
            all_symbols.append(symbol)

    slots = []

    for _ in range(cols):
        column = []
        remaining_symbols = all_symbols[:]
        for _ in range(rows):
            value = rd.choice(remaining_symbols)
            remaining_symbols.remove(value)
            column.append(value)
        slots.append(column)

    transposed_slots = []

    for row in range(rows):
        new_row = []
        for col in range(cols):
            new_row.append(slots[col][row])

        transposed_slots.append(new_row)

    return transposed_slots


def print_slot_machine(slots):
    for row in slots:
        print(" | ".join(row))


def check_winnings(slots, lines, bet, values):
    winnings = 0
    winning_lines = []

    for line in range(lines):
        row = slots[line]
        first_symbol = row[0]

        if all(symbol == first_symbol for symbol in row):
            winnings += values[first_symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def run_spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(
                "You do not have enough to bet that amount. "
                f"Your current balance is ${balance}."
            )

        else:
            break

    print(f"You are betting ${bet} on {lines} lines.")
    print(f"Total bet is ${total_bet}.")

    slots = get_slot_machine_spin(ROWS, COLS, SYMBOL_COUNT)
    print_slot_machine(slots)

    winnings, winning_lines = check_winnings(slots, lines, bet, SYMBOL_VALUE)
    print(f"You won ${winnings}.")

    if winning_lines:
        print(f"You won on lines: {', '.join(map(str, winning_lines))}")

    else:
        print("No winning lines this spin.")

    balance = balance - total_bet + winnings

    return balance


def main():
    balance = deposit_money()
    while True:
        print(f"Current balance is ${balance}.")

        if balance == 0:
            print("Your balance is $0. Game over.")
            print("You left with $0.")
            break

        answer = input("Press enter to play (q to quit).").strip().lower()

        if answer == "q":
            print(f"You left with ${balance}.")
            break

        balance = run_spin(balance)


if __name__ == "__main__":
    main()
