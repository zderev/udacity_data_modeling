# Project: Data Modeling with Postgres

  - Creating a Postgres database with tables designed to optimize queries on song play analysis
  - ETL pipeline for this analysis.

#### Datasets
We have two datasets - **Songs** and **Logs**.

The **Songs** dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID.
```
song_data/A/B/C/TRABCEI128F424C983.json
```
Example of a single song file, TRAABJL12903CDCF1A.json:
```python
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

The **Logs** dataset contains activity logs from a music streaming app based on specified configurations.
```
log_data/2018/11/2018-11-12-events.json
```

Tables structure

**Fact Table**
1. ***songplays*** - records in log data associated with song plays i.e. records with page NextSong
-- songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

**Dimension Tables**
2. ***users*** - users in the app. 
-- user_id, first_name, last_name, gender, level
3. ***songs*** - songs in music database
-- song_id, title, artist_id, year, duration
4. ***artists*** - artists in music database
-- artist_id, name, location, latitude, longitude
5. ***time*** - timestamps of records in songplays broken down into specific units
-- start_time, hour, day, week, month, year, weekday

#### 1. Creating Database and tables
```sh
$ python3 create_tables.py
```
#### 2. Run ETL process.
```sh
$ python3 etl.py
```
#### 3. Result
![](https://github.com/zderev/udacity_data_modeling/blob/master/result.jpg?raw=true)
