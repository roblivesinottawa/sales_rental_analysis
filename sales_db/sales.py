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
                            email_address VARCHAR(255) DEFAULT NULL,
                            number_of_complaints INT DEFAULT 0,
                            UNIQUE KEY (email_address));''')
            print("TABLE 'customers' CREATED SUCCESSFULLY.")
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS sales(
                            purchase_number INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            date_of_purchase DATE DEFAULT NULL,
                            customer_id INT(11) DEFAULT NULL,
                            item_code VARCHAR(10) DEFAULT NULL)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
            print("TABLE 'sales' CREATED SUCCESSFULLY.")
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS items(
                            item_code VARCHAR(255) NOT NULL,
                            item VARCHAR(255) NOT NULL,
                            unit_price DECIMAL(10,2) NOT NULL,
                            company_id VARCHAR(255) NOT NULL);''')
            print("TABLE 'items' CREATED SUCCESSFULLY.")
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS companies(
                            company_ID VARCHAR(255) PRIMARY KEY NOT NULL,
                            company_name VARCHAR(255) DEFAULT 'X',
                            headquarters_phone_number VARCHAR(255) NOT NULL,
                            UNIQUE KEY(headquarters_phone_number));''')
            print("TABLE 'companies' CREATED SUCCESSFULLY.")
            cursor.close()
            conn.close()
        except Error as e:
            print(e)
        
    def insert_customer(self, first_name, last_name, gender, email_address, number_of_complaints=0):
        '''this function inserts a customer'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO customers (
                            first_name, last_name, gender, email_address, number_of_complaints
                            ) 
                            VALUES 
                            (%s, %s, %s, %s, %s);''',
                            (first_name, last_name, gender, email_address, number_of_complaints))
            conn.commit()
            print("CUSTOMER ADDED SUCCESSFULLY.")
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def insert_sale(self, date_of_purchase, customer_id, item_code):
        '''this function will insert a sale'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO sales (
                            date_of_purchase, customer_id, item_code
                            ) 
                            VALUES 
                            (%s, %s, %s);''',
                            (date_of_purchase, customer_id, item_code))
            conn.commit()
            print("SALE ADDED SUCCESSFULLY.")
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def insert_item(self, item_code, item, unit_price, company_id):
        '''this function will insert an item'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO items (
                            item_code, item, unit_price, company_id
                            ) 
                            VALUES 
                            (%s, %s, %s, %s);''',
                            (item_code, item, unit_price, company_id))
            conn.commit()
            print("ITEM ADDED SUCCESSFULLY.")
            cursor.close()
            conn.close()
        except Error as e:
            print(e)
    
    def insert_company(self, company_id, company_name, headquarters_phone_number):
        '''this function will insert a company'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO companies (
                            company_ID, company_name, headquarters_phone_number
                            ) 
                            VALUES 
                            (%s, %s, %s);''',
                            (company_id, company_name, headquarters_phone_number))
            conn.commit()
            print("COMPANY ADDED SUCCESSFULLY.")
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def alter_table(self, table, column_name, column_type, column_name2):
        '''this function will alter random tables when invoked.'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute('''SHOW TABLES;''')
            tables = cursor.fetchall()
            print(tables)
            table = tables[1][0]
            cursor.execute("ALTER TABLE " + table + " ADD " + column_name + " " + column_type + "AFTER" + " " + column_name2 + ";")
            print("TABLE ALTERED SUCCESSFULLY.")
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

    def select_all(self, table):
        '''this function will select all from a table'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM " + table)
            rows = cursor.fetchall()
            print(rows)
            cursor.close()
            conn.close()
        except Error as e:
            print(e)
    
if __name__=='__main__':
    # create an instance of the class
    query = Sales('root', '', 'localhost', 'Sales')
    query.make_connection()

    # create a database
    # query.create_database()
    
    # create tables
    # query.create_table()

    # insert a customer
    # query.insert_customer('Peter', 'Figaro', 'M', 'peter@icloud.com')
    # query.insert_customer('Mary', 'Ford', 'F', 'maryford@icloud.com')

    # insert a sale
    # query.insert_sale('2020-01-01', '1', '1')

    # insert an item
    # query.insert_item('1', 'Macbook', '1000', '1')

    # insert a company
    # query.insert_company('1', 'Apple', '555-555-5555')

    # alter a table
    # query.alter_table("customers", "gender", "ENUM('M', 'F')", "last_name")

    # drop a table
    # query.drop_table()

    # select information
    query.select_all('customers')
    query.select_all('sales')
    query.select_all('companies')
    query.select_all('items')












   