-- Database Creation SQL
-- CREATE DATABASE vinyl_vault; omitted because Docker does this implicitly when the container is spun up

create table users (
    user_id int primary key,
    username varchar(255) not null,
    password_hash varchar(60) not null,
    country varchar(255),
    date_joined date not null
);

create table format (
    ftype varchar(255) primary key,
    fdescription text
);

create table album (
    album_id int primary key,
    title varchar(255) not null,
    release_date date null,
    label varchar(255),
    runtime varchar(4) not null  -- measured in minutes
);

create table song (
    song_id int primary key,
    title varchar(255) not null,
    is_explicit boolean not null default FALSE,
    duration int not null,  -- measured in minutes
    release_year int
);

create table artist (
    aname varchar(255),
    country varchar(255),
    debut_year int,
    is_active boolean not null default FALSE,

    constraint PK_artist primary key (aname, country, debut_year)
);

create table solo_artist (
    saname varchar(255),
    country varchar(255),
    debut_year int,
    firstname varchar(255) not null,
    lastname varchar(255) null,
    birthdate date null,
    instrument varchar(255) null,

    constraint PK_sartist primary key (saname, country, debut_year),
    constraint FK_sartist_artist foreign key (saname, country, debut_year) references artist(aname, country, debut_year) on delete cascade
);

create table band (
    bname varchar(255),
    country varchar(255),
    debut_year int,
    num_members int not null,
    formation_date date,
    breakup_date date,

    constraint PK_band primary key (bname, country, debut_year),
    constraint FK_band_artist foreign key (bname, country, debut_year) references artist(aname, country, debut_year) on delete cascade
);

create table album_format (
    format varchar(255),
    album_id int,

    constraint PK_aformat primary key (format, album_id),
    constraint FK_aformat_album foreign key (album_id) references album(album_id) on delete cascade,
    constraint FK_aformat_format foreign key (format) references format(ftype) on delete cascade
);

create table tracklisting (
    track_number int,
    album_id int,
    disc_number int,
    track_song int,

    constraint PK_tracklisting primary key (track_number, album_id),
    constraint FK_tracklisting_album foreign key (album_id) references album(album_id) on delete cascade,
    constraint FK_tracklisting_song foreign key (track_song) references song(song_id) on delete cascade
);

create table album_creation (
    artist_name varchar(255),
    artist_country varchar(255),
    artist_debut int,
    album_id int,

    constraint PK_acreation primary key (artist_name, artist_country, artist_debut, album_id),
    constraint FK_acreation_artist foreign key (artist_name, artist_country, artist_debut) references artist(aname, country, debut_year) on delete cascade,
    constraint FK_acreation_album foreign key (album_id) references album(album_id) on delete cascade
);

create table genre (
    gname varchar(255) primary key,
    gdescription text
);

create table album_genre (
    album_id int,
    genre_name varchar(255),

    constraint PK_agenre primary key (album_id, genre_name),
    constraint FK_agenre_album foreign key (album_id) references album(album_id) on delete cascade,
    constraint FK_agenre_genre foreign key (genre_name) references genre(gname) on delete cascade
);

create table song_genre (
    genre_name varchar(255),
    song_id int,

    constraint PK_sgenre primary key (genre_name, song_id),
    constraint FK_sgenre_genre foreign key (genre_name) references genre(gname) on delete cascade,
    constraint FK_sgenre_song foreign key (song_id) references song(song_id) on delete cascade
);

create table song_creation (
    artist_name varchar(255),
    artist_country varchar(255),
    artist_debut int,
    song_id int,

    constraint PK_screation primary key (artist_name, artist_country, artist_debut, song_id),
    constraint FK_screation_artist foreign key (artist_name, artist_country, artist_debut) references artist(aname, country, debut_year) on delete cascade,
    constraint FK_screation_song foreign key (song_id) references song(song_id) on delete cascade
);

create table collection (
    collection_id int primary key,
    collection_type varchar(10) not null 
        default 'General' 
        check (collection_type in ('General', 'Wishlist')),
    collection_name varchar(255) not null,
    date_created date not null,
    owned_by int not null,

    constraint FK_collection_user foreign key (owned_by) references users(user_id) on delete cascade
);

create table collection_song (
    song_id int,
    collection_id int,

    constraint PK_csong primary key (song_id, collection_id),
    constraint FK_csong_song foreign key (song_id) references song(song_id) on delete cascade,
    constraint FK_csong_collection foreign key (collection_id) references collection(collection_id) on delete cascade
);

create table collection_album (
    album_id int,
    collection_id int,

    constraint PK_calbum primary key (album_id, collection_id),
    constraint FK_calbum_album foreign key (album_id) references album(album_id) on delete cascade,
    constraint FK_calbum_collection foreign key (collection_id) references collection(collection_id) on delete cascade
);

create table song_rating (
    user_id int,
    song_id int,
    rating int null 
        default null 
        check (rating in (0, 1, 2, 3, 4, 5)),
    review text,
    date_added date not null,

    constraint PK_srating primary key (user_id, song_id),
    constraint FK_srating_user foreign key (user_id) references users(user_id) on delete cascade,
    constraint FK_srating_song foreign key (song_id) references song(song_id) on delete cascade
);

create table album_rating (
    user_id int,
    album_id int,
    rating int null 
        default null 
        check (rating in (0, 1, 2, 3, 4, 5)),
    review text,
    date_added date not null,

    constraint PK_arating primary key (user_id, album_id),
    constraint FK_arating_user foreign key (user_id) references users(user_id) on delete cascade,
    constraint FK_arating_song foreign key (album_id) references album(album_id) on delete cascade
);

