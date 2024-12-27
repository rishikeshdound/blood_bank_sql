import streamlit as st
from database_conn import get_db_connection
from management import *





def home_page():
    """Home page with navigation"""
    # st.title(f"Welcome To Donor Dashboard of , {st.session_state.username}")
    

   
    st.markdown(f"<h1 style='text-align: center;'>Welcome To  Dashboard of {st.session_state.username}!</h1>", unsafe_allow_html=True)
    
  

    if st.session_state.role == "Donor":
        donor_dashboard(st.session_state.username)  # Pass the username or user ID as required
    elif st.session_state.role == "Administrator":
        st.subheader("Administrator Dashboard")  # Placeholder for admin logic
        admin_dashboard(st.session_state.username)
    elif st.session_state.role == "Recipient":
        st.subheader("Recipient Dashboard")  # Placeholder for recipient logic
        recipient_dashboard(st.session_state.username)
    else:
        st.error("Invalid role detected. Please log in again.")
        if st.button("Log Out"):
            st.session_state.page = "login"
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()
    
   




def donor_dashboard(username):
    """Donor Dashboard"""


   
    
    st.sidebar.header("Donor Menu")
    options = ["View Profile", "Edit Profile", "Donation History", "Upcoming Campaigns"]
    choice = st.sidebar.radio("Choose an option", options)

    if choice == "View Profile":
        
        
        view_profile(username)
   
    elif choice == "Edit Profile":
        st.subheader("Edit Your Profile")
        
        edit_profile(username)
    elif choice == "Donation History":
        st.subheader("View Donation History")
        st.info("Donation history will be fetched and displayed here.")
        # donation_history(user_name)
        history = fetch_donation_history(username)

        if history:
            for record in history:
                st.text(f"Date: {record[0]}")
                st.text(f"Blood Type: {record[1]}")
                st.text(f"Units Donated: {record[2]}")
                st.text(f"Campaign: {record[3]}\n")
        else:
            st.info("No donation history found.")
    elif choice == "Upcoming Campaigns":
        st.subheader("Upcoming Campaigns")

        upcoming_campaigns(username)
    # Logout
    if st.sidebar.button("Logout"):
        st.session_state.page = "login"
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()


# ############ admin dashboard / page



def admin_dashboard(username):
    """Admin Dashboard"""
    st.sidebar.header("Admin Menu")
    options = [
        "View Profile",
        "Manage Blood Requests",
        "Manage Campaigns",
        "View Donors",
        "View Recipients",
        "Logout"
    ]
    choice = st.sidebar.radio("Choose an option", options)
    if choice == "View Profile":
        
        view_profile(username)
    elif choice == "Manage Blood Requests":
        st.subheader("Manage Blood Requests")
        manage_blood_requests()
    elif choice == "Manage Campaigns":
        st.subheader("Manage Campaigns")
        manage_campaigns()
    elif choice == "View Donors":
        st.subheader("View Donors")
        view_donors()
    elif choice == "View Recipients":
        st.subheader("View Recipients")
        view_recipients()
    elif choice == "Logout":
        st.session_state.page = "login"
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()




# recipient dashboard



def recipient_dashboard(username):
    """Recipient Dashboard"""

    st.sidebar.header("Recipient Menu")
    options = [
        "View Profile" , 
        "Request Blood",
        "View Blood Requests",
        "Blood Group Availability",
        "Edit Profile",
        "Logout",
    ]
    choice = st.sidebar.radio("Choose an option", options)


    if choice == "View Profile":
        view_profile(username)
    elif choice == "Request Blood":
        request_blood(username)
    elif choice == "View Blood Requests":
        view_blood_requests(username)
    elif choice == "Blood Group Availability":
        blood_available()
    elif choice == "Edit Profile":
        st.subheader("Edit Your Profile")
        
        edit_profile(username)
    elif choice == "Logout":
        st.session_state.page = "login"
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()




# fun for blood req

def request_blood(username):
    """Allows a recipient to request blood"""
    st.subheader("Request Blood")
    
    # Select Blood Group
    blood_group = st.selectbox("Select Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    units_required = st.number_input("Enter Units of Blood Required", min_value=1, step=1)
    reason = st.text_area("Reason for Request")
    
    if st.button("Submit Request"):
        cursor.execute(
            '''
            INSERT INTO blood_requests (user_id, blood_group, units_required, reason, request_status)
            VALUES ((SELECT user_id FROM users WHERE username = %s), %s, %s, %s, 'Pending')
            ''',
            (username, blood_group, units_required, reason)
        )
        conn.commit()
        st.success("Blood request submitted successfully!")



# 

def view_blood_requests(username):
    """View blood requests made by the recipient"""
    st.subheader("Your Blood Requests")
    
    cursor.execute(
        '''
        SELECT request_id, blood_group, units_required, reason, request_status, created_at
        FROM blood_requests
        WHERE user_id = (SELECT user_id FROM users WHERE username = %s)
        ORDER BY created_at DESC
        ''',
        (username,)
    )
    requests = cursor.fetchall()
    
    if requests:
        for req in requests:
            st.write(f"Request ID: {req[0]}")
            st.write(f"Blood Group: {req[1]}")
            st.write(f"Units Required: {req[2]}")
            st.write(f"Reason: {req[3]}")
            st.write(f"Status: {req[4]}")
            st.write(f"Created At: {req[5]}")
            st.write("---")
    else:
        st.info("No blood requests found.")
