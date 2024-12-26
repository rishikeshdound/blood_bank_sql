import streamlit as st
from authentication1 import create_user, auth_user
from database_conn import setup_table
from home import home_page

# Initialize database
setup_table()

# Session state initialization
if "page" not in st.session_state:
    st.session_state.page = "login"
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None

def login_page():
    """Login and Signup Page"""
    st.title("Blood Bank Management System")
    choice = st.radio("Choose an option:", ["Log In", "Sign Up"])


    if choice =="Sign Up":
        st.subheader("Create a New Account")

        with st.form(key='signup_form'):
        
        # basic auth details

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["Donor", "Administrator","Recipient"])

            # if new user fill all the details 

            col1 , col2 =st.columns(2)
            with col1:
                full_name = st.text_input("Full Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone Number")
            with col2:
                blood_group = st.selectbox("Blood Group" , ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                date_of_birth = st.date_input("Date of Birth")
            
            address = st.text_area("Address")

        
            submit_button = st.form_submit_button(label ="Sign Up")
            
            if submit_button:

                result = create_user(
                    username=username, 
                    password=password, 
                    role=role,
                    full_name = full_name,
                    email=email,
                    phone=phone,
                    blood_group=blood_group,
                    gender=gender,
                    date_of_birth=date_of_birth,
                    address=address
                )

            if "successful" in result:
                st.success(result)
                    # Optional: Automatically switch to login
                st.balloons()
                #    redirecting to loging page
            else:
                st.error(result)



                
               
    elif choice == "Log In":
        st.subheader("Log In to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Log In"):
            if username and password:
                role = auth_user(username, password)
                if role:
                    st.session_state.username = username
                    st.session_state.role = role  # Directly use role
                    st.session_state.page = "home"
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please enter username and password")

# Main application flow
def main():
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "home":
        home_page()

if __name__ == "__main__":
    main()