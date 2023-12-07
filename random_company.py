import json
import psycopg2
import requests
import random

connection = psycopg2.connect(
        host = "localhost",
        database = "google_itc",
        user = "yeraly",
        password = "123",
        port = "5432"
    )
cursor = connection.cursor()

cursor.execute("SELECT MAX(id) FROM person")
max_id = cursor.fetchone()

cursor.execute("SELECT MAX(id) FROM company")
max_id_company = cursor.fetchone()

for i in range(1, max_id[0]+1):
    cursor.execute(
        f"UPDATE person SET profession_id = {random.randint(1, max_id_company[0])}\
            WHERE id = {i}"
    )

    print(f"Пользователь {i} получил работу")

connection.commit()
cursor.close()
connection.close()