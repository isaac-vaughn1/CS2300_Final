from db_ops import get_connection
from screen_logic import login_screen, main_screen


def main():
    conn = get_connection()
    
    cur_user = -1

    while True:  # runs until hitting sys.exit() within either login_screen() or main_screen()
        cur_user = login_screen(conn)
        
        if cur_user != -1:
            main_screen(conn, cur_user)

    conn.close()

if __name__ == "__main__":
    main()
