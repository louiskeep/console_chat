import mysql.connector
import os


def check_login(username, userpassword):
    user = os.environ.get('AWS_USERNAME')
    pw = os.environ.get('AWS_PW')
    host = os.environ.get('AWS_HOST')

    try:
        with mysql.connector.connect(user=user, password=pw, host=host) as con:
            cursor = con.cursor()
            q = "USE userdata;"
            cursor.execute(q)
            q = f"SELECT password, username FROM userdata WHERE username = '{username}';"
            cursor.execute(q)
            result = cursor.fetchall()
            return result[0][0] == userpassword

    except Exception as e:
        print(e)
        return False


def check_register(username, password):
    user = os.environ.get('AWS_USERNAME')
    pw = os.environ.get('AWS_PW')
    host = 'userauthentication.c7xiltckrktp.us-east-2.rds.amazonaws.com'

    try:
        with mysql.connector.connect(user=user, password=pw, host=host) as con:
            cursor = con.cursor()
            q = "USE userdata;"
            cursor.execute(q)
            q = f"INSERT INTO userdata (username, password) VALUES ('{username}', '{password}');"
            cursor.execute(q)
            con.commit()
            return '/user registered'

    # Catch "unique entry" error
    # User already exists
    except mysql.connector.IntegrityError as e:
        print(e)
        return '/user already exists'
