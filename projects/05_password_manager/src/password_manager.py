from pathlib import Path

from cryptography.fernet import Fernet

project_dir = Path(__file__).parent.parent
data_dir = project_dir / "data"
key_file = data_dir / "key.key"
passwords_file = data_dir / "passwords.txt"


def ensure_data_dir():
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)


def load_or_create_key():
    if key_file.exists():
        key = key_file.read_bytes()
    else:
        key = Fernet.generate_key()
        key_file.write_bytes(key)

    return key


def add_password(fernet):
    account_name = input("Account name: ").strip()
    if not account_name:
        print("Account name cannot be empty.")
        return

    password = input("Password: ").strip()
    if not password:
        print("Password cannot be empty.")
        return

    encrypted_password = fernet.encrypt(password.encode())
    with passwords_file.open("a", encoding="utf-8") as f:
        f.write(f"{account_name}|{encrypted_password.decode()}\n")

    print("Password saved.")


def view_passwords(fernet):
    if not passwords_file.exists():
        print("No passwords saved yet.")
        return

    saved_passwords = [
        line.strip()
        for line in passwords_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not saved_passwords:
        print("No passwords saved yet.")
        return

    for line in saved_passwords:
        account_name, encrypted_password = line.split("|", 1)
        password = fernet.decrypt(encrypted_password.encode()).decode()
        print(f"Account: {account_name} | Password: {password}")


def main():
    ensure_data_dir()
    key = load_or_create_key()
    fernet = Fernet(key)

    while True:
        mode_text = input(
            "Would you like to add a new password, view existing passwords, or quit? "
        )
        mode = mode_text.strip().lower()

        if mode == "add":
            add_password(fernet)

        elif mode == "view":
            view_passwords(fernet)

        elif mode == "q":
            print("Goodbye!")
            break

        else:
            print("Invalid mode. Please type add, view, or q.")


if __name__ == "__main__":
    main()
