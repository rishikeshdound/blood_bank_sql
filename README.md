# Blood Bank Management System

A web-based application to streamline blood bank management processes, allowing donors, recipients, and admins to interact efficiently. The system supports Donor registration, Blood Recipient registration and a Admin registration  managed through a user-friendly interface.

---

##  Features

### 1. **Donor Functionalities**
- **Register/Sign In:** Donors can register or log in to their accounts.
- **Update Availability:** Mark themselves available for specific campaigns.
- **View Campaigns:** Access a list of upcoming blood donation campaigns.

### 2. **Recipient Functionalities**
- **Request Blood:** Submit a request for a specific blood type.
- **View Status:** Check the status of their blood requests.

### 3. **Admin Functionalities**
- **Approve/Reject Requests:** Manage blood requests submitted by recipients.
- **Manage Campaigns:** Add, update, or delete upcoming blood donation campaigns.

---

## 📂 Project Structure
- `newapp.py/`: Contains the core Streamlit application files.
- `database_conn.py/`: Includes SQL scripts for database creation and data management.
- `home.py/`: Includes Function Callings based on Roles and respective Functionalities. 
- `management.py/`: Includes Functionalities and queries .
- `README.md`: Documentation for the project.

---

## 🛠️ Technology Stack
- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend:** Python
- **Database:** pymysql

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rishikeshdound/blood_bank_sql.git
   cd blood_bank_sql
