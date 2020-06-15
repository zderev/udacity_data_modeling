import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Song file processing. As a result, data is written to the artists and songs tables.
    
    :param str cur: cursor to interact with the Postgres database
    :param str filepath: json file contains metadata about a song and the artist of that song.
    """
    
    # open json song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_id = df.song_id.values[0]
    title = df.title.values[0]
    artist_id = df.artist_id.values[0]
    year = int(df.year.values[0])
    duration = float(df.duration.values[0])
    
    song_data = (song_id, title, artist_id, year, duration)
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_id = df.artist_id.values[0]
    name = df.artist_name.values[0]
    location = df.artist_location.values[0]
    latitude = float(df.artist_latitude.values[0])
    longitude = float(df.artist_longitude.values[0])
    
    artist_data = (artist_id, name, location, latitude, longitude)
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Log file processing. As a result, data is written to the users and songplays tables.
    
    :param str cur: cursor to interact with the Postgres database
    :param str filepath: json file contains activity logs from a music streaming app
    """
    
    # open log file
    df = pd.read_json(filepath, lines=True)
    
    # filter by NextSong action
    df = df[df["page"] == 'NextSong'].reset_index(drop=True)

    # convert timestamp column to datetime
    t = df.ts.apply(pd.to_datetime, unit='ms')
    
    # insert time data records
    time_data = [[x, int(x.hour), int(x.day), int(x.weekofyear), int(x.month), int(x.year), int(x.weekday())] for x in t]
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(time_data, columns=column_labels) 

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (int(row.ts), int(row.ts), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    
    """Main function to perform ETL process"""
    
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()