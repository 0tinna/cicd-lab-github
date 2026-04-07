from flask import Flask, jsonify
from psycopg2 import pool
import os

app = Flask(__name__)
VERSION = os.environ.get('APP_VERSION', 'v1')
db_pool = None


def get_db_pool():
    global db_pool
    if db_pool is None:
        db_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=4,
            host=os.environ.get('POSTGRES_HOST', 'postgres'),
            dbname=os.environ.get('POSTGRES_DB', 'appdb'),
            user=os.environ.get('POSTGRES_USER', 'appuser'),
            password=os.environ.get('POSTGRES_PASSWORD', 'lab_db_password'),
        )
    return db_pool


@app.get('/healthz')
def healthz():
    return jsonify(status='ok', version=VERSION)


@app.get('/')
def index():
    return jsonify(message='cicd-lab-broken', version=VERSION)


@app.get('/dbcheck')
def dbcheck():
    conn = None
    try:
        conn = get_db_pool().getconn()
        with conn.cursor() as cur:
            cur.execute('select 1')
            row = cur.fetchone()
        return jsonify(status='ok', db=row[0], version=VERSION)
    except Exception as exc:
        return jsonify(
            status='error',
            error='database_unavailable',
            detail=exc.__class__.__name__,
        ), 503
    finally:
        if conn is not None:
            get_db_pool().putconn(conn)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
