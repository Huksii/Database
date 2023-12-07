import json
import psycopg2
import requests
import random

URL = 'https://randomuser.me/api/'

# response = requests.get(URL)
# data = response.json()

# with open ("user.json", "w", encoding= "UTF-8") as file:
#     json.dump(data, file, indent= 4, ensure_ascii=False)

def get_data(url=URL):
    response = requests.get(url)
    data = response.json()
    return data

def processing(user):
    professions = [ "engineer", "teacher", "scientist", "developer", "programmer", "artist", "designer", "nurse", "doctor", "lawyer", "firefighter", "police officer", "psychologist", "actor", "musician", "farmer", "hairdresser", "gardener", "electrician", "mechanic", "chef", "architect", "accountant", "librarian", "banker", "pilot", "flight attendant", "photographer", "sports coach", "journalist", "psychiatrist", "interior designer", "surgeon", "general practitioner", "construction engineer", "geologist", "astronomer", "physicist", "chemist", "historian", "lawyer", "judge", "company director", "taxi driver", "waiter", "bartender", "masseuse", "psychotherapist", "dentist", "veterinarian", "animator", "realtor", "sailor", "music teacher", "physical education teacher", "surveyor", "dentist surgeon", "economist", "builder", "porter"
]
    connection = psycopg2.connect(
        host = "localhost",
        database = "google_itc",
        user = "yeraly",
        password = "123",
        port = "5432"
    )
    cursor = connection.cursor()

    data = user['results'][0]
    appeal = data['name']['title']
    first_name = data['name']['first']
    last_name = data['name']['last']
    gender = data['gender']
    birth_date = data['dob']['date']
    age = data['dob']['age']
    phone = data['phone']
    location_street = f"{data['location']['street']['name']}, {data['location']['street']['number']}"
    city = data['location']['city']
    state = data['location']['state']
    country = data['location']['country']
    email = data['email']
    profession = random.choice(professions)
    salary = random.randint(60000, 2000000)

    cursor.execute("CREATE TABLE IF NOT EXISTS person(\
        id SERIAL PRIMARY KEY,\
        appeal VARCHAR(30) DEFAULT NULL,\
        first_name VARCHAR(255) DEFAULT NULL,\
        last_name VARCHAR(255) DEFAULT NULL,\
        gender VARCHAR(125) DEFAULT NULL,\
        birth_date VARCHAR(255) DEFAULT NULL,\
        age INT DEFAULT NULL,\
        phone VARCHAR(255) DEFAULT NULL,\
        street VARCHAR(355) DEFAULT NULL,\
        city VARCHAR(155) DEFAULT NULL,\
        state VARCHAR(355) DEFAULT NULL,\
        country VARCHAR(255) DEFAULT NULL,\
        email VARCHAR(255) DEFAULT NULL,\
        profession VARCHAR(255) DEFAULT NULL,\
        salary BIGINT DEFAULT NULL)")
    
    cursor.execute("INSERT INTO person(\
        appeal, first_name, last_name, gender, birth_date,\
        age, phone, street, city, state, country, email,\
        profession, salary) VALUES (%s, %s, %s, %s, %s,\
        %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (appeal, first_name, last_name, gender, birth_date, age,
         phone, location_street, city, state, country, email,
         profession, salary))
    
    connection.commit()
    cursor.close()
    connection.close()

def Run():
    for count in range(1,601):
        user = get_data()
        processing(user)
        print(f"Пользователь с номером {count} записан")

Run()