import getpass
import pandas as pd
import os
import sys
from datetime import datetime
from menus import *
from db_ops import *

def clear():
    """
    Clears console
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def login_screen(conn) -> int:
    """
    Handles the user choice logic behind the intro menu. Used to create a new account or login

    Args:
        conn: the postgres database connector object

    Returns:
        int: The current user ID for tracking throughout the program
    """
    curr = conn.cursor()

    cur_user = -1
    run = True
    while (run):
        menu_choice = intro_menu()

        # -----Login Menu Choice-----
        match menu_choice:
            # Log into the system
            case '1':
                username = input("Enter username: ")
                password = getpass.getpass("Enter password: ")

                login_success, cur_user = verify_user(curr, username, password)  # (bool, int) --> (user login success, userid)
                if login_success:
                    clear()
                    print("Log in successful!")
                    run = False
                else:
                    clear()
                    print("Incorrect username or password")

            # Create a new user
            case '2':
                create_success, cur_user = create_user(curr, register_menu())
                if create_success:
                    conn.commit()
                    clear()
                    print("User successfully created")
                    run = False
                else:
                    conn.rollback()
                    clear()
                    print("That user already exists")

            # Exit program
            case '3':
                sys.exit()

            case _:
                clear()
                print("Enter a valid option")
    
    return cur_user


def main_screen(conn, cur_user: int):
    """
    Handles the user choice logic behind the main menu. Exits main menu if the current user ever becomes invalid (-1)

    Args:
        conn: the postgres database connector object
        cur_user (int): the current user's ID from the database
    """
    run = True
    while (run):
        menu_choice = main_menu()

        # -----Main Menu Choice-----
        match menu_choice:
            # Search For Items
            case '1':
                clear()
                search_for = search_menu()

                if search_for in {"song", "album", "artist"}:
                    search_screen(conn, search_for, cur_user)
                else:
                    clear()
                    print("Invalid search parameter")

            # Collections Menu
            case '2':
                manage_collections_screen(conn, cur_user)

            # User Profile
            case '3':
                profile_info = get_user(conn.cursor(), cur_user)
                cur_user = profile_screen(conn, cur_user, profile_info)

            # Add Item
            case '4':
                add_item_screen(conn, cur_user)

            # Exit Program
            case '5':
                sys.exit()

            case _:
                clear()
                print("Enter a valid option")

        if cur_user == -1:
            clear()
            run = False


def search_screen(conn, search_for: str, cur_user: int):
    """
    Handles the user choice logic behind searching

    Args:
        conn: the postgres database connector object
        search_for (str): the type of item a user has chosen to search for (album/artist/song)
        cur_user (int): the current user's ID from the database
    """
    item = input(f"Enter {search_for} name: ").strip()
    rows, cols = search_item(conn.cursor(), search_for, item)

    run = True
    while (run):
        print_table(rows, cols)
        menu_choice = search_res_options()

        # -----Search result Menu Choice-----
        match menu_choice:
            # Add Song/Album to Collection
            case '1':
                if len(rows) > 1:
                    clear()
                    print("Narrow search to single item before adding to collection")
                elif len(rows) > 0:
                    if search_for in {"song", "album"}:
                        add_to_collection_screen(conn, cur_user, search_for, rows[0][0])  # rows[0][0] is the <album/song>_id val
                    else:
                        clear()
                        print("Cannot add this item to a collection")
                else:
                    clear()
                    print("No results to add to collection")

            # Rate Item
            case '2':
                if len(rows) > 1:
                    clear()
                    print("Narrow search to single item before rating")
                elif len(rows) > 0:
                    if search_for in {"song", "album"}:
                        rate_item_screen(conn, cur_user, search_for, rows[0][0])
                    else:
                        clear()
                        print("Cannot rate this item")
                else:
                    clear()
                    print("No results to rate")

            # Back
            case '3':
                clear()
                run = False


def profile_screen(conn, cur_user: int, profile_info: tuple[list[tuple], list[str]]) -> int:
    """
    Handles the user choice logic behind the profile screen

    Args:
        conn: the postgres database connector object
        cur_user (int): the current user's ID from the database
        profile_info (tuple[list[tuple], list[str]]): a tuple full of profile info retrieved from the db; formatted as (user_info_tuples, list_of_headers)

    Returns:
        int: The current user value; may be set to -1 to indicate logging out or deletion of account
    """
    rows, cols = profile_info

    run = True
    while (run):
        print_table(rows, cols)
        menu_choice = profile_menu()

        # -----Profile Menu Choice-----
        match menu_choice:
            # Edit Username
            case '1':
                new_uname = input("Enter username: ").strip()

                if (update_username(conn.cursor(), new_uname, cur_user)):
                    conn.commit()
                    clear()
                    print("Username update successful")
                else:
                    conn.rollback()
                    clear()
                    print("Failed to update username :(")

                rows, cols = get_user(conn.cursor(), cur_user)

            # Logout of account  
            case '2':
                cur_user = -1
                pass

            # Delete account
            case '3':
                if (delete_user(conn.cursor(), cur_user)):
                    conn.commit()
                    cur_user = -1
                else:
                    conn.rollback()
                    clear()
                    print("Failed to delete user. An error occurred")

            # Go Back to Main Menu
            case '4':
                clear()
                run = False

            case _:
                clear()
                print("Enter a valid option")

        if cur_user == -1:
            run = False

    return cur_user



def add_to_collection_screen(conn, cur_user: int, table: str, id: int):
    """
    Handles the user choice logic behind the collection addition screen

    Args:
        conn: the postgres database connector object
        cur_user (int): the current user's ID from the database
        table (str): the collection table to add to (song/album)
        id (int): the current collection's id
    """
    rows, cols = get_collections(conn.cursor(), cur_user)

    collection_ids = {row[0] for row in rows}

    run = True
    while (run):
        print_table(rows, cols)
        menu_choice = int(input("Enter collection ID to Add (0 to exit): ").strip())

        # Add Item to Collection
        if menu_choice in collection_ids:
            run = False
            clear()

            if add_to_collection(conn.cursor(), menu_choice, table, id):
                conn.commit()
                clear()
                print("Successfully added to collection!")
            else:
                conn.rollback()
                clear()
                print("Failed to add item to collection")

        # Back to Main
        elif menu_choice == 0:
            clear()
            run = False

        else:
            clear()
            print("Invalid option")


def rate_item_screen(conn, cur_user: int, table: str, id: int):
    """
    Handles the user choice logic behind the rate item screen

    Args:
        conn: the postgres database connector object
        cur_user (int): the current user's ID from the database
        table (str): the rating table to add to (song/album)
        id (int): the current item's id
    """
    run = True
    while (run):
        rating = int(input("Enter a rating (1-5): ").strip())
        if rating not in range(1, 6):  # range of [1, 6)
            clear()
            print("Invalid rating")
            continue

        review = input("Write a review (optional): ").strip()
        
        if add_rating(conn.cursor(), cur_user, rating, review, table, id):
            conn.commit()
            clear()
            print("Successfully added rating!")
        else:
            conn.rollback()
            clear()
            print("Failed to rate item")

        run = False


def manage_collections_screen(conn, cur_user: int):
    """
    Handles the user choice logic behind the collection manager screen

    Args:
        conn: the postgres database connector object
        cur_user (int): the current user's ID from the database
    """
    rows, cols = get_collections(conn.cursor(), cur_user)

    collection_ids = {row[0] for row in rows}

    update_happened = False
    run = True
    while (run):
        if update_happened:
            rows, cols = get_collections(conn.cursor(), cur_user)

        print_table(rows, cols)
        menu_choice = int(input("Enter collection ID to View (0 to exit): ").strip())

        # View Collection Contents
        if menu_choice in collection_ids:
            update_happened = view_collection_screen(conn, get_collection_info(conn.cursor(), menu_choice), menu_choice)

        # Back to Main
        elif menu_choice == 0:
            clear()
            run = False

        else:
            clear()
            print("Invalid option")


def view_collection_screen(conn, collection_info: tuple[list[tuple], list[str]], collection_id: int) -> bool:
    """
    Handles the user choice logic behind the collection viewer screen. 

    Args:
        conn: the postgres database connector object
        collection_info (tuple[list[tuple], list[str]]): a tuple full of collection info retrieved from the db; formatted as (collection_info_tuples, list_of_headers)
        collection_id (int): the current collection's id

    Returns:
        bool: a flag to indicate whether an update to the collection happened. Will be used to indicate if loaded collection results should be reloaded
    """
    rows, cols = collection_info

    update_happened = False
    run = True
    while (run):
        print_table(rows, cols)

        menu_choice = manage_collection_menu()

        match menu_choice:
            # Rename Collection
            case '1':
                new_name = input("Enter collection name: ").strip()

                if (update_collection_name(conn.cursor(), new_name, collection_id)):
                    update_happened = True
                    conn.commit()
                    clear()
                    print("Collection name update successful")
                else:
                    conn.rollback()
                    clear()
                    print("Failed to update collection name :(")

                rows, cols = get_collection_info(conn.cursor(), collection_id) 

            # Delete Collection
            case '2':
                if delete_collection(conn.cursor(), collection_id):
                    conn.commit()
                    clear()
                    update_happened = True
                    run = False
                    print("Collection deleted")
                else:
                    conn.rollback()
                    clear()
                    print("Failed to delete collection")

            # Go Back
            case '3':
                clear()
                run = False

            case _:
                clear()
                print("Enter a valid option")

    return update_happened


def add_item_screen(conn, cur_user: int):
    """
    Handles the user choice logic behind the add item screen

    Args:
        conn: the postgres database connector object
        cur_user (int): the current user's id
    """
    run = True
    while (run):
        menu_choice = add_item_menu()

        match menu_choice:
            # Add Format
            case '1':
                format_type = input("Enter format type: ").strip()
                format_desc = input("Enter format description: ").strip()
                if add_format(conn.cursor(), format_type, format_desc):
                    conn.commit()
                    clear()
                    print("Format added!")
                else:
                    conn.rollback()
                    clear()
                    print("Failed to add format :(")

            # Add Genre
            case '2':
                genre = input("Enter genre name: ").strip()
                genre_desc = input("Enter genre description: ").strip()
                if add_genre(conn.cursor(), genre, genre_desc):
                    conn.commit()
                    clear()
                    print("Genre added!")
                else:
                    conn.rollback()
                    clear()
                    print("Failed to add genre :(")
            
            # Add Song
            case '3':
                add_song_screen(conn)

            # Add Album
            case '4':
                add_album_screen(conn)

            # Add Artist
            case '5':
                add_artist_screen(conn)

            # Add Collection
            case '6':
                add_collection_screen(conn, cur_user)

            # Go Back
            case '7':
                clear()
                run = False

            case _:
                clear()
                print("Enter a valid option")


def add_song_screen(conn):
    """
    Handles the user choice logic behind the add song screen

    Args:
        conn: the postgres database connector object
    """
    song_title = input("Enter song title: ").strip()

    is_explicit = False
    while True:
        is_explicit = input("Does this song contain explicit material (y/n): ").strip().lower()
        if is_explicit in {"y", "yes"}:
            is_explicit = True
            break
        elif is_explicit in {"n", "no"}:
            is_explicit = False
            break
        else:
            print("Please enter y or n")

    song_duration = int(input("How long is the song (in minutes): "))

    release_date = None
    while True:
        val = input("Enter song release date (yyyy/mm/dd): ").strip()

        if release_date == "":  # allow null release date
            release_date = None
            break

        try:
            release_date = datetime.strptime(val, "%Y/%m/%d").date()
            break
        except ValueError:
            print("\nInvalid date. Please use format yyyy/mm/dd")

    if add_song(conn.cursor(), song_title, is_explicit, song_duration, release_date):
        conn.commit()
        clear()
        print("Song added!")
    else:
        conn.rollback()
        clear()
        print("Failed to add song :(")


def add_album_screen(conn):
    """
    Handles the user choice logic behind the add album screen

    Args:
        conn: the postgres database connector object
    """
    album_title = input("Enter album title: ").strip()

    release_date = None
    while True:
        val = input("Enter album release date (yyyy/mm/dd): ").strip()

        if release_date == "":  # allow null release date
            release_date = None
            break

        try:
            release_date = datetime.strptime(val, "%Y/%m/%d").date()
            break
        except ValueError:
            print("\nInvalid date. Please use format yyyy/mm/dd")

    label = input("What music label released this album: ")

    album_runtime = int(input("How long is the album (in minutes): "))

    if add_album(conn.cursor(), album_title, release_date, label, album_runtime):
        conn.commit()
        clear()
        print("Album added!")
    else:
        conn.rollback()
        clear()
        print("Failed to add album :(")


def add_artist_screen(conn):
    """
    Handles the user choice logic behind the add artist screen

    Args:
        conn: the postgres database connector object
    """
    artist_name = input("Enter artist name: ").strip()
    artist_country = input("Enter artist country: ").strip()

    debut_year = None
    while True:
        val = input("Enter artist debut year (yyyy): ").strip()

        if val.isdigit() and len(val) == 4:
            debut_year = int(val)
            break
        else:
            print("\nInvalid date. Please use format yyyy")

    is_active = False
    while True:
        is_active = input("Is this artist still active (y/n): ").strip().lower()
        if is_active in {"y", "yes"}:
            is_active = True
            break
        elif is_active in {"n", "no"}:
            is_active = False
            break
        else:
            print("Please enter y or n")

    if add_artist(conn.cursor(), artist_name, artist_country, debut_year, is_active):
        conn.commit()
        clear()

        while True:
            artist_class = input("Is this artist in a band, solo, or other (b/s/o): ").strip().lower()
            match artist_class:
                case "b":
                    num_members = int(input("How many band members: ").strip())

                    if add_band(conn.cursor(), artist_name, artist_country, debut_year, num_members):
                        conn.commit()
                        clear()
                        print("Artist registered as \"Band\"")
                        break
                    else:
                        conn.rollback()
                        clear()
                        print("Failed to register artist class :(")

                case "s":
                    fname = input("Enter artist real first name: ").strip()

                    if add_solo_artist(conn.cursor(), artist_name, artist_country, debut_year, fname):
                        conn.commit()
                        clear()
                        print("Artist registered as \"Solo Artist\"")
                        break
                    else:
                        conn.rollback()
                        clear()
                        print("Failed to register artist class :(")

                case "o":
                    print("Artist added!")
                    break

                case _:
                    print("Enter a valid option")

    else:
        conn.rollback()
        clear()
        print("Failed to add artist :(")



def add_collection_screen(conn, cur_user: int):
    """
    Handles the user choice logic behind the add collection screen

    Args:
        conn: the postgres database connector object
        cur_user (int): the current user's db id
    """
    is_wishlist = False
    while True:
        is_wishlist = input("Is this collection a wishlist (y/n): ").strip().lower()
        if is_wishlist in {"y", "yes"}:
            is_wishlist = True
            break
        elif is_wishlist in {"n", "no"}:
            is_wishlist = False
            break
        else:
            print("Please enter y or n")

    coll_name = input("Enter collection name: ").strip()

    if add_collection(conn.cursor(), is_wishlist, coll_name, cur_user):
        conn.commit()
        clear()
        print("Collection created!")
    else:
        conn.rollback()
        clear()
        print("Failed to create collection :(")



def print_table(rows: list[tuple], cols: list[str]):
    """
    Prints pandas dataframe version of retrieved table data

    Args:
        rows (list[tuple]): a list of the retrieved rows
        cols (list[str]): a list of headers
    """
    df = pd.DataFrame(rows, columns=cols)

    if df.empty:
        print("No results found")
    else:
        print("\n" + df.to_string(index=False, justify="left"))
