import os

import pymysql
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

load_dotenv()
app = FastAPI()


def get_connection():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.get("/api/servers")
def list_servers():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, hostname, ip_address, environment, description "
                "FROM servers"
            )
            return cur.fetchall()
    finally:
        conn.close()


app.mount("/", StaticFiles(directory="static", html=True), name="static")
