# Project 05 - Password Manager

Status: Completed.

This project is a command-line password manager practice project. It stores account names with encrypted passwords in local ignored files. It is intended for learning file I/O, simple command modes, and basic encryption workflow, not for production password storage.

## Goal

Build a small terminal program that:

- lets the user choose between adding a password, viewing saved passwords, or quitting,
- stores account names and encrypted passwords in a local data file,
- creates or loads an encryption key from a local key file,
- decrypts saved passwords only when viewing them,
- handles invalid modes clearly,
- keeps generated key and password data out of version control.

## Learning Focus

- reading from and writing to files,
- appending structured text records,
- creating helper functions,
- using the `cryptography` package,
- encrypting and decrypting strings with Fernet,
- command-mode loops,
- keeping local secret data out of Git.

## Run Command

From the repository root:

```powershell
python projects/05_password_manager/src/password_manager.py
```

## Expected Terminal Interaction

Add password example:

```text
Would you like to add a new password, view existing passwords, or quit? add
Account name: email
Password: example-password
Password saved.
Would you like to add a new password, view existing passwords, or quit? q
Goodbye!
```

View password example:

```text
Would you like to add a new password, view existing passwords, or quit? view
Account: email | Password: example-password
Would you like to add a new password, view existing passwords, or quit? q
Goodbye!
```

Invalid mode example:

```text
Would you like to add a new password, view existing passwords, or quit? delete
Invalid mode. Please type add, view, or q.
Would you like to add a new password, view existing passwords, or quit? q
Goodbye!
```

## Completion Checklist

- The program can be run from the terminal.
- The user can add a password.
- The user can view saved passwords.
- Invalid modes are handled without crashing.
- Password data is written to a local file.
- Password data is encrypted before it is stored.
- Generated key and password files are ignored by Git.

## Notes

- Local password data is stored under `projects/05_password_manager/data/`.
- `key.key` and `passwords.txt` are ignored by Git and should not be committed.
- This project is for practice only. Do not use it to store real passwords.
