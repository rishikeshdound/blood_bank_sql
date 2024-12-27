import streamlit as st
import pymysql  # Use pymysql instead of mysql.connector
from hashlib import sha256
from database_conn import get_db_connection



# Function to sign up a new user with hashed password
def create_user(username, password, role,full_name =None , email=None , phone = None , blood_group = None , gender =None , date_of_birth = None ,address = None ):
    conn = get_db_connection()
    cursor = conn.cursor()
    hash_password = sha256(password.encode()).hexdigest()

    try:


        query = '''insert into users (username ,password , role ,full_name , email , phone, blood_group , gender , date_of_birth, address) values (%s, %s, %s,%s, %s, %s,%s, %s, %s ,%s)'''

        cursor.execute(query, (
                       username, hash_password, role,full_name ,email,phone,blood_group,gender,date_of_birth,address  )
                    )
        conn.commit()
    except pymysql.MySQLError as e:
        return f"Error: {str(e)}"
    finally:
        conn.close()

    return "Registration successful! Log into your account."


# Function to authenticate a user
def auth_user(username, password):
    try :
        conn = get_db_connection()
        cursor = conn.cursor()
        hash_password = sha256(password.encode()).hexdigest()
        
        cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", 
                    (username, hash_password))

        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except pymysql.MySQLError as err:
        print(f"Authentication error: {err}")
        return None


# Streamlit app to sign up or log in users

