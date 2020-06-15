
# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES
songplay_table_create = ("""
    
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id bigint NOT NULL, 
        start_time timestamp NOT NULL, 
        user_id int NOT NULL,
        level varchar NOT NULL, 
        song_id varchar, 
        artist_id varchar, 
        session_id int NOT NULL, 
        location varchar, 
        user_agent varchar,
        UNIQUE (songplay_id, user_id)
        );
        """)

user_table_create = ("""
    
    CREATE TABLE IF NOT EXISTS users (
        user_id int PRIMARY KEY, 
        first_name varchar NOT NULL, 
        last_name varchar NOT NULL, 
        gender varchar, 
        level varchar NOT NULL
        );
        """)

song_table_create = ("""

    CREATE TABLE IF NOT EXISTS songs (
        song_id varchar PRIMARY KEY, 
        title varchar NOT NULL, 
        artist_id varchar NOT NULL, 
        year int NOT NULL, 
        duration float NOT NULL);
""")

artist_table_create = ("""

    CREATE TABLE IF NOT EXISTS artists (
        artist_id varchar PRIMARY KEY, 
        name varchar NOT NULL, 
        location varchar, 
        latitude float, 
        longitude float);
""")

time_table_create = ("""
    
    CREATE TABLE IF NOT EXISTS time (
        start_time timestamp PRIMARY KEY, 
        hour int, 
        day int, 
        week int, 
        month int, 
        year int, 
        weekday int);
    
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays (
        songplay_id, 
        start_time, 
        user_id, 
        level, 
        song_id, 
        artist_id, 
        session_id, 
        location, 
        user_agent
        )
    VALUES (%s, TO_TIMESTAMP(%s::double precision / 1000), %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
""")

user_table_insert = ("""
    INSERT INTO users (
        user_id, 
        first_name, 
        last_name, 
        gender, 
        level
        )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level
""")

song_table_insert = ("""    
    INSERT INTO songs (
        song_id, 
        title, 
        artist_id, 
        year, 
        duration
        )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
""")

artist_table_insert = ("""
    INSERT INTO artists (
        artist_id, 
        name, 
        location, 
        latitude, 
        longitude
        )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO UPDATE SET name=EXCLUDED.name, location=EXCLUDED.location, latitude=EXCLUDED.latitude, longitude=EXCLUDED.longitude
""")

time_table_insert = ("""
    INSERT INTO time (
        start_time, 
        hour, 
        day, 
        week, 
        month, 
        year, 
        weekday
        )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
""")

# FIND SONGS
song_select = ("""
    SELECT 
        t1.song_id, 
        t1.artist_id 
    FROM 
        songs t1 JOIN artists t2 ON t1.artist_id = t2.artist_id
    WHERE 
        t1.title = %s 
        and t2.name = %s 
        and t1.duration = %s
""")

# QUERY LISTS

create_table_queries = [
    songplay_table_create, 
    user_table_create, 
    song_table_create, 
    artist_table_create, 
    time_table_create
]
drop_table_queries = [
    songplay_table_drop, 
    user_table_drop, 
    song_table_drop, 
    artist_table_drop, 
    time_table_drop
]