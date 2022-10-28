import sqlite3 as sql


def activate_foreign_keys(con):
    query = f'''PRAGMA foreign_keys = ON;'''.strip()

    con.execute(query)


def create_tables(connection):
    con = sql.connect(connection)

    activate_foreign_keys(con)

    query = f'''CREATE TABLE IF NOT EXISTS people (
            id          INTEGER PRIMARY KEY,
            name        TEXT NOT NULL
        );'''.strip()

    con.execute(query)

    query = f'''CREATE TABLE IF NOT EXISTS training (
            id          INTEGER PRIMARY KEY,
            p_id        INTEGER NOT NULL,
            coords      TEXT NOT NULL,
            time        INTEGER NOT NULL,
            distance    REAL NOT NULL,
            speed       REAL NOT NULL,
            date        TEXT NOT NULL,
            description TEXT,

            FOREIGN KEY (p_id) REFERENCES people (id)
        );'''.strip()

    con.execute(query)

    query = f'''CREATE TABLE IF NOT EXISTS friends (
            p_id        INTEGER NOT NULL,
            f_id        INTEGER NOT NULL,

            FOREIGN KEY (p_id) REFERENCES people (id),
            FOREIGN KEY (f_id) REFERENCES people (id),
            PRIMARY KEY (p_id,f_id)
        );'''.strip()

    con.execute(query)

    query = f'''CREATE TABLE IF NOT EXISTS images (
            id          INTEGER PRIMARY KEY,
            t_id        INTEGER NOT NULL,
            image       BLOB NOT NULL,

            FOREIGN KEY (t_id) REFERENCES training (id)
        );'''.strip()

    con.execute(query)
    con.close()


def drop_tables(connection):
    con = sql.connect(connection)

    activate_foreign_keys(con)

    query = f'''DROP TABLE IF EXISTS friends;'''.strip()
    con.execute(query)

    query = f'''DROP TABLE IF EXISTS images;'''.strip()
    con.execute(query)

    query = f'''DROP TABLE IF EXISTS training;'''.strip()
    con.execute(query)

    query = f'''DROP TABLE IF EXISTS people;'''.strip()
    con.execute(query)

    con.close()


def select(connection, table_name, search):
    con = sql.connect(connection)

    activate_foreign_keys(con)

    query = f'''SELECT {search} FROM {table_name};
    '''.strip()

    cur = con.cursor()
    cur.execute(query)
    print(query)
    print(cur.fetchall())
    cur.close()
    con.close()


def create_triggers(connection):
    con = sql.connect(connection)

    activate_foreign_keys(con)

    query = f'''
    CREATE TRIGGER IF NOT EXISTS add_friend
    AFTER INSERT ON friends
    BEGIN
        INSERT INTO friends (p_id,f_id) VALUES (NEW.f_id,NEW.p_id);
    END;
    '''.strip()

    con.execute(query)
    con.close()


def insert_people(connection, name):
    con = sql.connect(connection)

    activate_foreign_keys(con)

    query = f'''INSERT INTO people (name) VALUES (\'{name}\');
            '''.strip()

    con.execute(query)
    con.commit()
    con.close()


def insert_friend(connection, m_id, f_id):
    con = sql.connect(connection)

    activate_foreign_keys(con)

    query = f'''INSERT INTO friends (p_id,f_id) VALUES ({m_id},{f_id});
            '''.strip()

    con.execute(query)
    con.commit()
    con.close()


def insert_training(connection, p_id, coords, time_sec, dist_km, speed, date, description, images):
    con = sql.connect(connection)

    activate_foreign_keys(con)
    coords = str(coords).replace('\'', '')

    query = f'''
            INSERT INTO training (p_id, coords, time, distance, speed, date, description) 
            VALUES ({p_id},\'{coords}\',{time_sec},{dist_km},{speed},\'{date}\',\'{description}\');
            '''.strip()

    con.execute(query)
    con.commit()

    query = f'''SELECT COUNT(*) FROM training;
    '''.strip()

    cur = con.cursor()
    cur.execute(query)
    t_id = cur.fetchone()[0]
    cur.close()

    for image in images:
        query = '''INSERT INTO images (t_id,image) VALUES (?,?);
                    '''.strip()
        data = (t_id, open(image, 'rb').read())

        con.execute(query, data)
        con.commit()

    con.close()


if __name__ == '__main__':
    db_name = 'cm'
    drop_tables(db_name)
    create_tables(db_name)
    create_triggers(db_name)
    insert_people(db_name, 'Roberto')
    insert_people(db_name, 'Ana')
    insert_people(db_name, 'José')
    insert_people(db_name, 'Filipe')
    insert_friend(db_name, 1, 4)
    insert_training(db_name, 1, ['40.5 / 23', '40.6 / 23.1'], 100, 0.2, 2, '2022-10-19 13:24:22.123',
                    'Very good training session!', ['C:\\Users\\rober\\Downloads\\eu2.jpg'])
    select(db_name, 'people', '*')
    select(db_name, 'training', '*')
    select(db_name, 'friends', '*')
    select(db_name, 'images', 't_id')
