import psycopg2

def get_connection():
    try:
        return psycopg2.connect(
            database="vinyl_vault",
            user="student",
            password="pass123",
            host="localhost",
            port=5500,
        )
    except Exception as e:
        print("Connection error:", e)
        return None


def check_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """)
    
    tables = cursor.fetchall()
    print("Tables:", tables)


# --- main flow ---
conn = get_connection()

if conn:
    print("Connection to PostgreSQL established successfully.")
    check_tables(conn)
else:
    print("Connection failed.")
