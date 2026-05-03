-- A bit of seed data so the application is in a usable state as soon as the container is spun up

insert into genre (gname, gdescription) values
    ('Hip-Hop', 'Rap and hip-hop music'),
    ('Indie Rock', 'Independent rock music'),
    ('Jazz-Funk', 'Fusion of jazz and funk grooves');


insert into format (ftype, fdescription) values
    ('Digital', 'Streaming or digital download'),
    ('Vinyl', 'Vinyl record');


insert into artist (aname, country, debut_year, is_active) values
    ('J. Cole', 'USA', 2007, TRUE),
    ('Little Brother', 'USA', 2001, FALSE),
    ('Foxtide', 'USA', 2020, TRUE),
    ('Incognito', 'UK', 1979, TRUE);


insert into solo_artist (saname, country, debut_year, firstname, lastname) values
    ('J. Cole', 'USA', 2007, 'Jermaine', 'Cole');


insert into band (bname, country, debut_year, num_members) values
    ('Foxtide', 'USA', 2020, 4),
    ('Incognito', 'UK', 1979, 6);


insert into album (title, release_date, label, runtime) values
    ('Friday Night Lights', '2010-11-12', 'Roc Nation', 60),
    ('The Minstrel Show', '2005-09-13', 'Atlantic', 70),
    ('Entropy', '2023-01-01', 'Independent', 45),
    ('Positivity', '1993-01-01', 'Talkin Loud', 55);


insert into album_creation (artist_name, artist_country, artist_debut, album_id) values
    ('J. Cole', 'USA', 2007, 1),
    ('Little Brother', 'USA', 2001, 2),
    ('Foxtide', 'USA', 2020, 3),
    ('Incognito', 'UK', 1979, 4);


insert into song (title, is_explicit, duration, release_date) values
    ('Too Deep for the Intro', TRUE, 3, '2010-11-12'),
    ('Lovin'' It (feat. Joe Scudda)', TRUE, 4, '2005-09-13'),
    ('Heart in the Ground', FALSE, 3, '2023-01-01'),
    ('Inversions', FALSE, 5, '1993-01-01');


insert into song_creation (artist_name, artist_country, artist_debut, song_id) values
    ('J. Cole', 'USA', 2007, 1),
    ('Little Brother', 'USA', 2001, 2),
    ('Foxtide', 'USA', 2020, 3),
    ('Incognito', 'UK', 1979, 4);


insert into tracklisting (track_number, album_id, disc_number, track_song) values
    (2, 1, 1, 1),
    (10, 2, 1, 2),
    (6, 3, 1, 3),
    (1, 4, 1, 4);


insert into album_genre (album_id, genre_name) values
    (1, 'Hip-Hop'),
    (2, 'Hip-Hop'),
    (3, 'Indie Rock'),
    (4, 'Jazz-Funk');


insert into song_genre (genre_name, song_id) values
    ('Hip-Hop', 1),
    ('Hip-Hop', 2),
    ('Indie Rock', 3),
    ('Jazz-Funk', 4);


insert into album_format (format, album_id) values
    ('Digital', 1),
    ('Digital', 2),
    ('Digital', 3),
    ('Vinyl', 2),
    ('Vinyl', 4);


insert into users (username, password_hash, country, date_joined) values
    ('test', '$2b$12$tswnnQ/8myyEfNHnhtjJkOyOIkM4lgN18kiUOhy6keXL3V.3/SMSy', 'USA', '2026-05-02');


insert into collection (collection_type, collection_name, date_created, owned_by) values
    ('General', 'Late Night Vibes', '2026-05-02', 1);


insert into collection (collection_type, collection_name, date_created, owned_by) values
    ('Wishlist', 'Vinyl Wants', '2026-05-02', 1);


insert into collection_song (song_id, collection_id) values
    (1, 1),
    (3, 1);


insert into collection_album (album_id, collection_id) values
    (1, 1),
    (3, 1);


insert into collection_song (song_id, collection_id) values
    (2, 2);


insert into collection_album (album_id, collection_id) values
    (2, 2);


insert into song_rating (user_id, song_id, rating, review, date_added) values
    (1, 1, 5, 'Classic intro track energy', '2026-05-04'),
    (1, 2, 5, 'Slept on song from a slept on album', '2026-05-02'),
    (1, 3, 3, 'Beautiful indie sound', '2026-05-01');


insert into album_rating (user_id, album_id, rating, review, date_added) values
    (1, 1, 5, 'One of J. Cole''s best early projects', '2026-05-02'),
    (1, 2, 5, 'Underrated classic', '2026-05-02'),
    (1, 3, 3, 'Strong indie debut vibes', '2026-05-02');
