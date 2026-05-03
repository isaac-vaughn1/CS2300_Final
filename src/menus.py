import getpass

def register_menu() -> tuple[str, str]:
    username = input("Enter username: ").strip()
    password = getpass.getpass("Enter password: ")

    return (username, password)


def intro_menu() -> str:
    print("\n-----WELCOME TO VINYL VAULT-----")
    print("1. Log  In")
    print("2. Create Account")
    print("3. Exit")

    return input("> ").strip()


def main_menu() -> str:
    print("\n-----MAIN MENU-----")
    print("1. Search Item")
    print("2. Collections")
    print("3. Profile")
    print("4. Add Item")
    print("5. Exit")

    return input("> ").strip()


def search_menu() -> str:
    print("\n-----SEARCH-----")

    return input("Search for song/album/artist: ").strip().lower()

def search_res_options() -> str: 
    print("\n-----SEARCH RESULTS-----")
    print("1. Add to Collection")
    print("2. Rate")
    print("3. Back")

    return input("> ").strip()


def profile_menu() -> str:
    print("\n-----PROFILE-----")
    print("1. Edit Username")
    print("2. Logout")
    print("3. Delete Account")
    print("4. Back")

    return input("> ").strip()


def manage_collection_menu() -> str:
    print("\n-----COLLECTION MANAGER-----")
    print("1. Rename")
    print("2. Delete")
    print("3. Back")

    return input("> ").strip()


def add_item_menu() -> str:
    print("\n-----Add Item-----")
    print("1. Add Format")
    print("2. Add Genre")
    print("3. Add Song")
    print("4. Add Album")
    print("5. Add Artist")
    print("6. Add Collection")
    print("7. Back")

    return input("> ").strip()
