import psycopg2
import bcrypt

def get_connection():
    try:
        return psycopg2.connect(
            database="vinyl_vault",
            user="student",
            password="pass123",
            host="localhost",
            port=5500
        )
    except:
        return False


def create_user(curr, user_info: tuple[str,str]) -> tuple[bool, int]:
    username, password = user_info
    hashpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # don't allow duplicate usernames
    curr.execute(
        """
        select exists (
            select 1 from users where username = %s
        );
        """,
        (username,)
    )
    exists = curr.fetchone()[0]

    if exists:
        return (False, -1)
    
    # insert a new, valid user into the db
    try:
        curr.execute(
            """
            insert into users (username, password_hash, date_joined) values
                (%s, %s, current_date)
                returning user_id;
            """,
            (username, hashpw)
        )

        # need to grab the new user id so the system can acknowledge that as the current user
        user_id = curr.fetchone()[0]

        return (True, user_id)
    except Exception:
        return (False, -1)


def verify_user(curr, username: str, password: str) -> tuple[bool,int]:
    curr.execute(
        "select password_hash, user_id from users where username = %s;", 
        (username,)
    )
    row = curr.fetchone()
    
    if row is None:
        return (False, -1)
    
    stored_hash = row[0]

    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode()

    return (bcrypt.checkpw(password.encode(), stored_hash), row[1])


def search_item(curr, table: str, filter_val: str) -> tuple[list[tuple], list[str]]:
    if table in {"album", "song"}:
        query = f"select * from {table} where title like %s"
        curr.execute(query, (f"%{filter_val}%",))

    else:
        query = """select * from artist a
                   left join solo_artist sa on a.aname = sa.saname and a.country = sa.country and a.debut_year = sa.debut_year
                   left join band b on a.aname = b.bname and a.country = b.country and a.debut_year = b.debut_year
                   where coalesce (sa.saname, b.bname, a.aname) ilike %s;
                """
        curr.execute(query, (f"%{filter_val}%",))

    rows = curr.fetchall()
    cols = [desc[0] for desc in curr.description]

    return (rows, cols)


def get_user(curr, cur_user: int) -> tuple[list[tuple], list[str]]:
    curr.execute(
        """
        select u.username, u.country, u.date_joined,
            sr.avg_song_rating, ar.avg_album_rating, sr.max_song_rating, ar.max_album_rating,
            coalesce(c_stats.num_collections, 0) as num_collections,
            coalesce(c_stats.collected_songs, 0) as collected_songs,
            coalesce(c_stats.collected_albums, 0) as collected_albums
        from users u

        -- collection info
        left join (
            select c.owned_by as user_id, count(distinct c.collection_id) as num_collections, count(distinct cs.song_id) as collected_songs,
                count(distinct ca.album_id) as collected_albums
            from collection c
            left join collection_song cs on c.collection_id = cs.collection_id
            left join collection_album ca on c.collection_id = ca.collection_id
            group by c.owned_by
        ) c_stats on u.user_id = c_stats.user_id

        -- ratings info
        left join (
            select user_id, round(avg(rating), 2) as avg_song_rating, max(rating) as max_song_rating
            from song_rating
            group by user_id
        ) sr on u.user_id = sr.user_id

        left join (
            select user_id, round(avg(rating), 2) as avg_album_rating, max(rating) as max_album_rating
            from album_rating
            group by user_id
        ) ar on u.user_id = ar.user_id

        where u.user_id = %s;
        """,
        (cur_user,)
    )

    rows = curr.fetchall()
    cols = [desc[0] for desc in curr.description]

    return (rows, cols)


def update_username(curr, uname: str, cur_user: int) -> bool:
    curr.execute(
        """
        update users set username = %s where user_id = %s;
        """,
        (uname, cur_user)
    )

    return curr.rowcount > 0


def delete_user(curr, cur_user: int) -> bool:
    curr.execute(
        """
        delete from users where user_id = %s;
        """,
        (cur_user,)
    )

    return curr.rowcount > 0


def get_collections(curr, cur_user: int) -> tuple[list[tuple], list[str]]:
    curr.execute(
        """
        select collection_id, collection_name, collection_type
        from collection
        where owned_by = %s;
        """,
        (cur_user,)
    )

    rows = curr.fetchall()
    cols = [desc[0] for desc in curr.description]

    return (rows, cols)


def add_to_collection(curr, collection_id: int, table: str, item_id: int) -> bool:
    allowed_tables = {"song", "album"}
    if table not in allowed_tables:
        return False
    
    query = f"""
            insert into collection_{table} values
                (%s, %s);
            """
    try:
        curr.execute(query, (item_id, collection_id))
        return True
    except Exception:
        return False

def add_rating(curr, cur_user: int, rating: int, review: str, table: str, item_id: int) -> bool:
    allowed_tables = {"song", "album"}
    if table not in allowed_tables:
        return False
    
    query = f"""
            insert into {table}_rating (user_id, {table}_id, rating, review, date_added)
            values
                (%s, %s, %s, %s, current_date)
            on conflict(user_id, {table}_id)
            do update set
                rating = excluded.rating,
                review = excluded.review,
                date_added = current_date;
            """
    try:
        curr.execute(query, (cur_user, item_id, rating, review))
        return True
    except Exception:
        return False


def get_collection_info(curr, collection_id: int) -> tuple[list[tuple], list[str]]:
    curr.execute(
        """
        select c.collection_id, c.collection_name, c.collection_type, c.date_created,
            s.title as title,
            'song' as item_type,
            sr.rating as rating,
            s.release_date as release_date
        from collection c
        left join collection_song cs on c.collection_id = cs.collection_id
        left join song s on cs.song_id = s.song_id
        left join song_rating sr 
            on cs.song_id = sr.song_id and c.owned_by = sr.user_id
        where c.collection_id = %s and exists (
            select 1
            from collection_song cs2
            where cs2.collection_id = c.collection_id
        )

        union all

        select c.collection_id, c.collection_name, c.collection_type, c.date_created,
            a.title as title,
            'album' as item_type,
            ar.rating as rating,
            a.release_date
        from collection c
        left join collection_album ca on c.collection_id = ca.collection_id
        left join album a on ca.album_id = a.album_id
        left join album_rating ar 
            on ca.album_id = ar.album_id and c.owned_by = ar.user_id
        where c.collection_id = %s and exists (
            select 1
            from collection_album ca2
            where ca2.collection_id = c.collection_id
        );
        """,
        (collection_id, collection_id)
    )

    rows = curr.fetchall()
    cols = [desc[0] for desc in curr.description]

    return (rows, cols)


def delete_collection(curr, collection_id: int) -> bool:
    curr.execute(
        """
        delete from collection where collection_id = %s;
        """,
        (collection_id,)
    )

    return curr.rowcount > 0


def update_collection_name(curr, collection_name: str, collection_id: int) -> bool:
    curr.execute(
        """
        update collection set collection_name = %s where collection_id = %s;
        """,
        (collection_name, collection_id)
    )

    return curr.rowcount > 0


def add_format(curr, format: str, description: str) -> bool:
    try:
        curr.execute(
            """
            insert into format (ftype, fdescription) values 
                (%s, %s);
            """,
            (format, description)
        )
        return True
    except Exception:
        return False


def add_genre(curr, genre: str, description: str) -> bool:
    try:
        curr.execute(
            """
            insert into genre (gname, gdescription) values 
                (%s, %s);
            """,
            (genre, description)
        )
        return True
    except Exception:
        return False


def add_song(curr, title: str, is_explicit: bool, duration: int, release_date) -> bool:
    try:
        curr.execute(
            """
            insert into song (title, is_explicit, duration, release_date) values
                (%s, %s, %s, %s);
            """,
            (title, is_explicit, duration, release_date)
        )
        return True
    except Exception:
        return False


def add_album(curr, title: str, release_date, label: str, album_runtime: int) -> bool:
    try:
        curr.execute(
            """
            insert into album (title, release_date, label, runtime) values
                (%s, %s, %s, %s);
            """,
            (title, release_date, label, album_runtime)
        )
        return True
    except Exception:
        return False


def add_artist(curr, name: str, country: str, debut_year: int, is_active: bool) -> bool:
    try:
        curr.execute(
            """
            insert into artist (aname, country, debut_year, is_active) values
                (%s, %s, %s, %s);
            """,
            (name, country, debut_year, is_active)
        )
        return True
    except Exception:
        return False


def add_band(curr, name: str, country: str, debut_year: int, num_members: int) -> bool:
    try:
        curr.execute(
            """
            insert into band (bname, country, debut_year, num_members) values 
                (%s, %s, %s, %s);
            """,
            (name, country, debut_year, num_members)
        )
        return True
    except Exception:
        return False


def add_solo_artist(curr, name: str, country: str, debut_year: int, fname: str) -> bool:
    try:
        curr.execute(
            """
            insert into solo_artist (saname, country, debut_year, firstname) values
                (%s, %s, %s, %s);
            """,
            (name, country, debut_year, fname)
        )
        return True
    except Exception:
        return False


def add_collection(curr, is_wishlist: bool, name: str, cur_user: int) -> bool:
    type = "General"
    if is_wishlist:
        type = "Wishlist"

    try:
        curr.execute(
            """
            insert into collection (collection_type, collection_name, date_created, owned_by) values 
                (%s, %s, current_date, %s);
            """,
            (type, name, cur_user)
        )
        return True
    except Exception:
        return False
