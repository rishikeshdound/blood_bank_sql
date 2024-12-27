from database_conn import get_db_connection
import streamlit as st


conn = get_db_connection()
cursor = conn.cursor()

#  for profile view  
def fetch_profile(username):
    """Fetch donor profile details from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT full_name, email, phone, blood_group, gender, date_of_birth, address
        FROM users
        WHERE username = %s
        ''',
        (username,)
    )
    profile = cursor.fetchone()
    conn.close()
    return profile

# profile interface st
# common for all 

def view_profile(username):
    
    
    conn = get_db_connection()
    cursor = conn.cursor()

    st.subheader("Your Profile Details ")
    profile = fetch_profile(username)

    if profile:
        # Accessing the fields by their index
        st.write(f"**Full Name:** {profile[0]}")
        st.write(f"**Email:** {profile[1]}")
        st.write(f"**Phone Number:** {profile[2]}")
        st.write(f"**Blood Group:** {profile[3]}")
        st.write(f"**Gender:** {profile[4]}")
        st.write(f"**Date of Birth:** {profile[5]}")
        st.write(f"**Address:** {profile[6]}")
    else:
        st.write("Profile details not found.")

    cursor.close()






# for updating recors in db  profile  ------> used for all the users admin , donor , recipient 




def edit_profile(username):
    st.subheader("Edit Your Profile")
    
    # Fetch current profile details
    with get_db_connection() as conn: # 
        with conn.cursor() as cursor:
            cursor.execute("SELECT email, phone, address FROM users WHERE username = %s", (username,))
            profile = cursor.fetchone()
    
    if profile:
        with st.form(key='edit_profile_form'):
            email = st.text_input("Email", value=profile[0])
            phone = st.text_input("Phone Number", value=profile[1])
            address = st.text_area("Address", value=profile[2])
            
            submit_button = st.form_submit_button("Update Profile")
            
            if submit_button:
                # Update profile in the database
                with get_db_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "UPDATE users SET email = %s, phone = %s, address = %s WHERE username = %s",
                            (email, phone, address, username)
                        )
                        conn.commit()
                st.success("Profile updated successfully!")
                st.rerun()  # Refresh the page to reflect changes

    else:
        st.error("Profile details not found.")








# donation history table 

def fetch_donation_history(user_id):
    """Fetch donation history for a specific user"""
    conn = get_db_connection()
    cursor = conn.cursor()
# based on or username data is being fetched
    query = '''
        SELECT d.donation_date, d.blood_group, d.units_donated, c.name AS campaign_name
        FROM donations d
        LEFT JOIN campaigns c ON d.campaign_id = c.campaign_id
        WHERE d.user_id = %s
        ORDER BY d.donation_date DESC
    '''
    cursor.execute(query, (user_id))
    history = cursor.fetchall()
    conn.close()
    return history

    


# isme add a thing where user and just add checkbox to enroll for blood donation camp 


def view_campaigns():
    st.subheader("View Upcoming Campaigns")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all upcoming campaigns
    cursor.execute("SELECT * FROM campaigns ORDER BY date ASC")
    campaigns = cursor.fetchall()

    if campaigns:
        for campaign in campaigns:
            st.text(f"Campaign Name: {campaign[1]}")
            st.text(f"Date: {campaign[2]}")
            st.text(f"Location: {campaign[3]}")
            st.text(f"Description: {campaign[4]}")
            st.text("-" * 40)
    else:
        st.info("No upcoming campaigns found.")

    conn.close()


# 



# for marking intrest 




def mark_campaign_interest(username, campaign_id):
    """Mark donor's interest in a campaign."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user_id based on the username
    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    if not user:
        st.error("User not found.")
        return

    user_id = user[0]

    # Check if the user already marked interest
    cursor.execute(
        "SELECT * FROM campaign_interests WHERE user_id = %s AND campaign_id = %s",
        (user_id, campaign_id),
    )
    interest_exists = cursor.fetchone()

    if interest_exists:
        st.warning("You have already shown interest in this campaign.")
    else:
        # Insert the interest into the campaign_interests table
        cursor.execute(
            "INSERT INTO campaign_interests (user_id, campaign_id) VALUES (%s, %s)",
            (user_id, campaign_id),
        )
        conn.commit()
        st.success(f"Successfully marked interest in campaign ID: {campaign_id}.")

    conn.close()







# 


def upcoming_campaigns(username):
    st.subheader("Upcoming Donation Campaigns")
    
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # fetch all upcoming campaigns 
    cursor.execute("SELECT * FROM campaigns WHERE date >= CURDATE() ORDER BY date ASC")
    campaigns = cursor.fetchall()

    if campaigns:
        for campaign in campaigns:
            st.text(f"Campaign Name: {campaign[1]}")
            st.text(f"Date: {campaign[2]}")
            st.text(f"Location: {campaign[3]}")
            st.text(f"Description: {campaign[4]}")
            available_for_campaign = st.checkbox(f"Mark as available for {campaign[1]}", key=campaign[0])

            if available_for_campaign:
                # Save the donor's interest in the campaign
                mark_campaign_interest(username, campaign[0])

            st.text("-" * 40)
    else:
        st.info("No upcoming campaigns found.")

    conn.close()













# donation hist

def donation_history(donor_id):
    st.subheader("Your Donation History")
    
    cursor.execute(
        '''
        SELECT blood_type, units_donated, donation_date, campaign_name
        FROM donations
        WHERE donor_id = %s
        ORDER BY donation_date DESC
        ''',
        (donor_id,)
    )
    records = cursor.fetchall()
    conn.close()








    if records:
        for record in records:
            st.text(f"Date: {record[2]}")
            st.text(f"Blood Type: {record[0]}")
            st.text(f"Units Donated: {record[1]}")
            st.text(f"Campaign: {record[3]}\n")
    else:
        st.info("No donation history found.")












#  w###################### for admin functionality 








# view donors

def view_donors():
    """View donors filtered by blood group"""
    st.subheader("View Donors")
    
    # Dropdown for filtering by blood group
    blood_group_filter = st.selectbox("Filter by Blood Group", ["ALL", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    
    # SQL query based on the selected blood group
    if blood_group_filter == "ALL":
        query = '''
        SELECT user_id, full_name, blood_group
        FROM users
        WHERE role = 'donor'
        '''
        cursor.execute(query)
    else:
        query = '''
        SELECT user_id, full_name, blood_group
        FROM users
        WHERE role = 'donor' AND blood_group = %s
        '''
        cursor.execute(query, (blood_group_filter,))
    
    # Fetch results
    donors = cursor.fetchall()
    
    # Display the results
    if donors:
        st.write(f"Displaying donors for blood group: {blood_group_filter if blood_group_filter != 'ALL' else 'All Blood Groups'}")
        for donor in donors:
            st.write(f"User ID: {donor[0]}")
            st.write(f"Name: {donor[1]}")
            st.write(f"Blood Group: {donor[2]}")
            st.write("---")
    else:
        st.info(f"No donors found for blood group: {blood_group_filter}.")






# for blood group aval or inventrory we can call 



def blood_available():
    """Check availability of blood groups"""
    st.subheader("Availability of Blood Groups")
    
    
    query = '''
    SELECT blood_group, 
           SUM(units_donated) AS total_units, 
           COUNT(user_id) AS donor_count
    FROM donations
    GROUP BY blood_group
    ORDER BY blood_group
    '''
    cursor.execute(query)
    availability = cursor.fetchall()
    
    if availability:
       
        st.write("Blood Group Availability")
        st.table(
            {
                "Blood Group": [row[0] for row in availability],
                "Total Units": [row[1] for row in availability],
                "Donor Count": [row[2] for row in availability],
            }
        )
    else:
        st.info("No blood group availability data found.")




#  manage donations 
def manage_campaigns():
    """Manage donation campaigns"""
    action = st.radio("Choose an action", ["Add Campaign", "View/Edit/Delete Campaigns"])

    if action == "Add Campaign":
        name = st.text_input("Campaign Name")
        date = st.date_input("Campaign Date")
        location = st.text_input("Campaign Location")
        description = st.text_area("Campaign Description")
        if st.button("Add Campaign"):
            query = '''
            INSERT INTO campaigns (name, date, location, description)
            VALUES (%s, %s, %s, %s)
            '''
            cursor.execute(query, (name, date, location, description))
            conn.commit()
            st.success("Campaign added successfully.")

    elif action == "View/Edit/Delete Campaigns":
        query = '''
        SELECT campaign_id, name, date, location, description FROM campaigns
        '''
        cursor.execute(query)
        campaigns = cursor.fetchall()

        if campaigns:
            for campaign in campaigns:
                st.write(f"Campaign ID: {campaign[0]}")
                st.write(f"Name: {campaign[1]}")
                st.write(f"Date: {campaign[2]}")
                st.write(f"Location: {campaign[3]}")
                st.write(f"Description: {campaign[4]}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"Edit {campaign[0]}"):
                        edit_campaign(campaign[0])
                with col2:
                    if st.button(f"Delete {campaign[0]}"):
                        delete_campaign(campaign[0])
                st.write("---")
        else:
            st.info("No campaigns available.")

def delete_campaign(campaign_id):
    """Delete a campaign"""
    query = '''
    DELETE FROM campaigns WHERE campaign_id = %s
    '''
    cursor.execute(query, (campaign_id,))
    conn.commit()
    st.success(f"Campaign ID {campaign_id} deleted successfully.")

def edit_campaign(campaign_id):
    """Edit a campaign (functionality to be implemented)"""
    st.info(f"Edit functionality for Campaign ID {campaign_id} is under construction.")




# for seeing recipient request  and approving 

def manage_blood_requests():
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM blood_requests WHERE request_status = 'Pending'")
    requests = cursor.fetchall()

    if requests:
        for request in requests:
            st.text(f"Request ID: {request[0]}")
            st.text(f"User ID: {request[1]}")
            st.text(f"Blood Group: {request[2]}")
            st.text(f"Units Required: {request[3]}")
            st.text(f"Reason: {request[4]}")
            st.text(f"Requested At: {request[6]}")

            # Action buttons for admin
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Approve Request {request[0]}", key=f"approve_{request[0]}"):
                    cursor.execute(
                        "UPDATE blood_requests SET request_status = 'Approved' WHERE request_id = %s", 
                        (request[0],)
                    )
                    conn.commit()
                    st.success(f"Request ID {request[0]} approved.")

            with col2:
                if st.button(f"Reject Request {request[0]}", key=f"reject_{request[0]}"):
                    cursor.execute(
                        "UPDATE blood_requests SET request_status = 'Rejected' WHERE request_id = %s", 
                        (request[0],)
                    )
                    conn.commit()
                    st.error(f"Request ID {request[0]} rejected.")

            st.text("-" * 40)
    else:
        st.info("No pending blood requests found.")

    conn.close()


# for inserting donations 

