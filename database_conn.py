import pymysql

def get_db_connection():

    return pymysql.connect(
        host = "localhost" , 
        user = "root",
        password = "123456",
        database = "blood_bank"
    )




def setup_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    

    cursor.execute(
        '''
        CREATE TABLE if not exists users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    role ENUM('Donor', 'Administrator', 'Recipient') NOT NULL,
    blood_group VARCHAR(5),
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other'),
    address TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
)

        '''
     )   


# donor detail table

   
    
    #  donation history table  

    cursor.execute(

        '''
            CREATE TABLE IF NOT EXISTS  donations(
    donation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- References users table
    blood_group VARCHAR(5),
    units_donated INT,
    donation_date DATE,
    campaign_id INT,
    Foreign key (user_id) references users(user_id),
    foreign key (campaign_id) references campaigns(campaign_id)
)


        '''

    )


# campigns table 

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

        '''
    )




    cursor.execute('''
    CREATE TABLE IF NOT EXISTS blood_requests (
        request_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        blood_group VARCHAR(5) NOT NULL,
        units_required INT NOT NULL,
        reason TEXT,
        request_status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
''')




    conn.commit()
    conn.close()
    



    # blood recipient db 


#     cursor.execute( '''


#     CREATE TABLE IF NOT EXISTS blood_requests (
#     request_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     blood_group VARCHAR(5) NOT NULL,
#     units_required INT NOT NULL,
#     reason TEXT,
#     request_status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
# )'''
#                    )
    
#     conn.commit()
#     conn.close()