def create_table(connection):
    with connection.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS users(\
            id SERIAL PRIMARY KEY,\
            user_id BIGINT,\
            is_bot BOOLEAN,\
            first_name VARCHAR(255),\
            last_name VARCHAR(255),\
            username VARCHAR(255),\
            language_code VARCHAR(255),\
            is_premium BOOLEAN)")
        
        cursor.execute("CREATE TABLE IF NOT EXISTS msg(\
            id SERIAL PRIMARY KEY,\
            user_id BIGINT,\
            message TEXT)")
        
        connection.commit()

def add_message(connection, user_id, user_text):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO msg(\
            user_id, message) VALUES(%s, %s)",
        (user_id, user_text)
        )
        connection.commit()

def add_users(connection, user_id, first_name, last_name,
         username, is_bot, language_code, is_premium):
    
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO users(\
            user_id, first_name, last_name,\
            username, is_bot, language_code, is_premium)\
        VALUES(%s, %s, %s, %s, %s, %s, %s)",
        (user_id, first_name, last_name,
         username, is_bot, language_code, is_premium)
        )

        connection.commit()

def check_user(connection, user_id):
    with connection.cursor() as cursor:
        cursor.execute(f"select user_id from users \
                where user_id = {user_id}")
        
        db_check = cursor.fetchone()

        return db_check
    
def get_user_id(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_id from users")

        all_user_id = cursor.fetchall()

        s = []
        for i in all_user_id:
            s.extend(list(i))
        return s


