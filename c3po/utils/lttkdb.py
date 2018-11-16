import psycopg2
from c3po.config import config


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config('database.ini', 'postgresqlFirst')

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        conn.autocommit = True

        # create a cursor
        cur = conn.cursor()

        # create database if not exists
        cur.execute(
            "SELECT COUNT(*) = 0 FROM pg_catalog.pg_database WHERE datname = 'lttkgp'"
        )
        not_exists_row = cur.fetchone()
        not_exists = not_exists_row[0]
        if not_exists:
            print('Creating database "lttkgp"...')
            cur.execute('CREATE DATABASE lttkgp')
        cur.close()
        conn.close()

        print('connecting to lttkgp...')
        conn = psycopg2.connect(
            user=params['user'],
            database='lttkgp',
            host=params['host'],
            password=params['password'])
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
