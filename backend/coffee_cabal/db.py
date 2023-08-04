import psycopg2

import os

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

connection = psycopg2.connect(
    database="postgres",
    user=user,
    password=password,
    host=host,
    port=port,
)
