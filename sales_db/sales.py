from mysql.connector import connect, Error

class Sales:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def make_connection(self):
        '''This function establishes a connection to the database'''
        try:
            conn = connect(user=self.user, password=self.password, host=self.host, database=self.database)
            if conn.is_connected():
                print("CONNECTION ESTABLISHED SUCCESSFULLY.")
            return conn
        except Error as e:
            print(e)
    
    def create_database(self):
        '''This function creates a database'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS Sales")
            print("DATABASE CREATED SUCCESSFULLY.")
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def create_table(self):
        '''this function creates tables'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS customers(
                            customer_id INT AUTO_INCREMENT PRIMARY KEY,
                            first_name VARCHAR(255) NOT NULL,
                            last_name VARCHAR(255) NOT NULL,
                            email_address VARCHAR(255) NOT NULL,
                            number_of_complaints INT);''')
            print("TABLE 'customers' CREATED SUCCESSFULLY.")
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS sales(
                            purchase_number INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            date_of_purchase DATE DEFAULT NULL,
                            customer_id INT(11) DEFAULT NULL,
                            item_code VARCHAR(10) DEFAULT NULL,
                            FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
            print("TABLE 'sales' CREATED SUCCESSFULLY.")
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS items(
                            item_code VARCHAR(255) NOT NULL,
                            item VARCHAR(255) NOT NULL,
                            unit_price DECIMAL(10,2) NOT NULL,
                            company_id VARCHAR(255) NOT NULL);''')
            print("TABLE 'items' CREATED SUCCESSFULLY.")
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS companies(
                            company_ID VARCHAR(255) NOT NULL,
                            comapny_name VARCHAR(255) NOT NULL,
                            headquarters_phone_number INT(12) NOT NULL);''')
            print("TABLE 'companies' CREATED SUCCESSFULLY.")
            cursor.close()
            conn.close()
        except Error as e:
            print(e)
        
    def insert_customer(self, first_name, last_name, email_address, number_of_complaints):
        '''this function inserts a customer'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO customers (
                            first_name, last_name, email_address, number_of_complaints
                            ) 
                            VALUES 
                            (%s, %s, %s, %s);''',
                            (first_name, last_name, email_address, number_of_complaints))
            conn.commit()
            print("CUSTOMER ADDED SUCCESSFULLY.")
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

        def drop_table(self):
            '''this function will drop a random table if called'''
            try:
                conn = self.make_connection()
                cursor = conn.cursor()
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                table = tables[0][0]
                cursor.execute("DROP TABLE " + table)
                print("TABLE DROPPED SUCCESSFULLY.")
                cursor.close()
                conn.close()
            except Error as e:
                print(e)
        

query = Sales('root', 'mysqlpassmacrob', 'localhost', 'Sales')
# query.make_connection()
# query.create_database()
# query.create_table()
# query.insert_customer('John', 'Doe', 'john_doe@email.com', '5')











   