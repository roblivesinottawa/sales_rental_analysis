import mysql.connector
from mysql.connector import connect, Error

class Employees:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        self.cursor = self.make_connection()
    
    def make_connection(self):
        '''This function establishes a connection to the database'''
        try:
            conn = connect(user=self.user, password=self.password, host=self.host, database=self.database)
            ('CONNECTION FAILED' if conn.is_connected() == False else 'CONNECTION SUCCESSFULLY ESTABLISHED')
            return conn
        except Error as e:
            print(e)

    def show_database(self):
        '''This function shows the databases'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES;")
            [print(db) for db in cursor]
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def show_all_tables(self):
        '''This function displays the tables'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute("USE employees;")
            print("DATABASE 'employees' SELECTED SUCCESSFULLY.")
            cursor.execute("SHOW TABLES;")
            [print(table) for table in cursor]
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def show_table_content(self, table : str):
        '''This function will display a specific table in the database with an added constraint'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM %s LIMIT 20;" % table)
            [print(row) for row in cursor]
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def show_employees_with_parameter(self, parameter : str):
        '''This function will display all employees with a specific parameter'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees WHERE %s;" % parameter)
            [print(row) for row in cursor]
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def employees_with_same_salary(self, salary : int):
        '''This function will display employees with the same salary'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute(
            '''
            SELECT s.salary, t.title, e.first_name, e.last_name
            FROM salaries s
            INNER JOIN titles t
            ON s.emp_no = t.emp_no
            INNER JOIN employees e
            ON t.emp_no = e.emp_no
            WHERE s.salary = %s
            GROUP BY s.salary ORDER BY s.salary LIMIT 20;
            ''' % salary)
            [print(row) for row in cursor]
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def employees_salary_higher_than_120000(self, salary : int):
        '''This function will display employees with a salary higher than 120000'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute(
            '''
            SELECT s.salary, t.title, e.first_name, e.last_name
            FROM salaries s
            INNER JOIN titles t
            ON s.emp_no = t.emp_no
            INNER JOIN employees e
            ON t.emp_no = e.emp_no
            WHERE s.salary > %s
            GROUP BY s.salary ORDER BY s.salary LIMIT 20;
            ''' % salary)
            [print(row) for row in cursor]
            cursor.close()
            conn.close()
        except Error as e:
            print(e)


employees = Employees('root', '', 'localhost', 'employees')
employees.make_connection()
employees.show_database()
employees.show_all_tables() 
# employees.show_table_content('employees')
# employees.show_table_content('departments')
# employees.show_table_content('salaries')
# employees.show_employees_with_parameter('first_name = "John"')
# employees.show_employees_with_parameter('hire_date = "2000-01-01"')
employees.employees_with_same_salary(80000)
employees.employees_salary_higher_than_120000(120000)

