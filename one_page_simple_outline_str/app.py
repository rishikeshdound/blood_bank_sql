import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to establish MySQL connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='blood',
            user='root',  # Replace with your DB username
            password='123456'  # Replace with your DB password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
        return None

# Function to fetch data from a table
def fetch_data(query):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        records = cursor.fetchall()
        connection.close()
        return records

# Function to insert a new donor into the database
def add_donor(name, number, mail, age, gender, blood_group, address):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """
        INSERT INTO donor_details (donor_name, donor_number, donor_mail, donor_age, donor_gender, donor_blood, donor_address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (name, number, mail, age, gender, blood_group, address)
        cursor.execute(query, values)
        connection.commit()
        connection.close()
        st.success("Donor added successfully!")

# Streamlit UI
def main():
    st.title("Blood Bank Management System")

    # Menu options
    menu = ["Home", "View Donors", "Add Donor", "Contact Queries", "Admin Login"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to the Blood Bank Management System")
    
    elif choice == "View Donors":
        st.subheader("List of Donors")
        donors = fetch_data("SELECT * FROM donor_details")
        if donors:
            for donor in donors:
                st.write(f"Name: {donor['donor_name']}, Age: {donor['donor_age']}, Blood Group: {donor['donor_blood']}")
        else:
            st.info("No donors available.")
    
    elif choice == "Add Donor":
        st.subheader("Add a New Donor")
        donor_name = st.text_input("Donor Name")
        donor_number = st.text_input("Donor Contact Number")
        donor_mail = st.text_input("Donor Email")
        donor_age = st.number_input("Donor Age", min_value=18, max_value=65, step=1)
        donor_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        donor_blood = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        donor_address = st.text_area("Donor Address")

        if st.button("Submit"):
            if donor_name and donor_number and donor_age and donor_gender and donor_blood and donor_address:
                add_donor(donor_name, donor_number, donor_mail, donor_age, donor_gender, donor_blood, donor_address)
            else:
                st.error("Please fill all the fields.")

    elif choice == "Contact Queries":
        st.subheader("Contact Queries")
        queries = fetch_data("SELECT * FROM contact_query")
        if queries:
            for query in queries:
                st.write(f"Name: {query['query_name']}, Query: {query['query_message']}, Status: {query['query_status']}")
        else:
            st.info("No contact queries available.")
    
    elif choice == "Admin Login":
        st.subheader("Admin Login")
        admin_username = st.text_input("Username")
        admin_password = st.text_input("Password", type='password')
        
        if st.button("Login"):
            query = f"SELECT * FROM admin_info WHERE admin_username = '{admin_username}' AND admin_password = '{admin_password}'"
            admin = fetch_data(query)
            if admin:
                st.success("Login Successful!")
                # Additional functionality for admin after login can be added here
            else:
                st.error("Invalid credentials!")

if __name__ == '__main__':
    main()
