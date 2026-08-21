import getpass

from utils.database import create_user, find_user_by_email, init_database


def main():
    init_database()
    name = input("Admin name: ").strip()
    email = input("Admin email: ").strip().lower()
    password = getpass.getpass("Admin password (8+ characters): ")

    if len(password) < 8:
        raise SystemExit("Password must contain at least 8 characters.")
    if find_user_by_email(email):
        raise SystemExit("An account with that email already exists.")

    create_user(name, email, password, role="admin")
    print(f"Admin account created for {email}.")


if __name__ == "__main__":
    main()
