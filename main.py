from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db import get_connection

app = FastAPI()

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
