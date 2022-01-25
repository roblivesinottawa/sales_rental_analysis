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

    def employees_gender(self):
        "this function will display the employees gender as Male and Female"
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT 
                    emp_no, first_name, last_name,
                CASE
                    WHEN gender = 'M' THEN 'Male'
                ELSE 'Female'
                END AS gender
                FROM employees LIMIT 20;
                '''
            )
            [print(row) for row in cursor]
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def get_salary_difference(self, value1=30000, value2=20000):
        '''This function will display the difference between the highest and lowest salaries'''
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute(
            '''
            SELECT e.emp_no, e.first_name, e.last_name,
            MAX(s.salary) - MIN(s.salary) AS salary_difference,
            CASE
                WHEN MAX(s.salary) - MIN(s.salary) > %s THEN
                'Salary was raised by more than %s'
                WHEN MAX(s.salary) - MIN(s.salary) 
                BETWEEN %s AND %s THEN
                'Salary was raised by more than %s but less than %s'
                ELSE 'Salary was raised by less than %s'
            END AS Salary_increase
            FROM dept_manager dm 
            JOIN employees e
            ON e.emp_no = dm.emp_no
            JOIN salaries s
            ON s.emp_no = dm.emp_no
            GROUP BY S.emp_no;
            ''', (value1, value1, value2, value1, value2, value1, value2))
            [print(row) for row in cursor]
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def is_current_employee(self):
        "This function will display employees and if they are still with the company or not"
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT
                    e.emp_no, e.first_name, e.last_name,
                CASE
                    WHEN MAX(de.to_date) > sysdate()
                    THEN 'Still with the company'
                    ELSE 'Not with the company'
                    END AS is_current_employee
                FROM employees e
                JOIN dept_emp de
                ON e.emp_no = de.emp_no
                GROUP BY e.emp_no
                LIMIT 20;
                '''
            )
            [print(row) for row in cursor]
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def employee_maximum_salary(self, emp_no : int):
        "This function will display the maximum salary of an employee"
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT s1.* 
                FROM salaries AS s1 
                LEFT JOIN salaries AS s2
                ON (s1.emp_no = s2.emp_no AND s1.from_date < s2.from_date)
                WHERE s2.emp_no IS NULL AND s1.emp_no = %s;
                ''' % emp_no
            )
            [print(row) for row in cursor]
            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def employee_salary_display(self):
        "This function will display the salary of an employee"
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT e.emp_no, e.first_name, e.last_name, s.salary, s.from_date
                FROM employees e
                INNER JOIN
                (SELECT emp_no, MAX(salary) AS SALARY, FROM_DATE 
                FROM salaries GROUP BY emp_no) s
                ON (e.emp_no = s.emp_no) LIMIT 20;
                ''' 
            )
            [print(row) for row in cursor]
            cursor.close()
            conn.close()
        except Error as e:
            print(e)
    
    def salary_per_title(self):
        "this function will display salaries for each title descendingly"
        try:
            conn = self.make_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT new_table.title, MAX(new_table.salary) AS salary
                FROM (
                    SELECT e.first_name, e.last_name, s.salary AS salary, t.title AS title
                    FROM employees e
                    INNER JOIN (
                        SELECT emp_no, MAX(salary) AS salary FROM salaries GROUP BY emp_no
                    ) s
                    ON s.emp_no = e.emp_no
                    INNER JOIN titles t
                    ON t.emp_no = e.emp_no
                )
                new_table GROUP BY new_table.title
                ORDER BY salary DESC;
                '''
            )
            [print(row) for row in cursor]
            cursor.close()
            conn.close()
        except Error as e:
            print(e)


employees = Employees('root', 'mysqlpassmacrob', 'localhost', 'employees')
employees.make_connection()
employees.show_database()
employees.show_all_tables() 
# employees.show_table_content('employees')
# employees.show_table_content('departments')
# employees.show_table_content('salaries')
# employees.show_employees_with_parameter('first_name = "John"')
# employees.show_employees_with_parameter('hire_date = "2000-01-01"')
# employees.employees_with_same_salary(80000)
# employees.employees_salary_higher_than_120000(120000)
# employees.employees_gender()
# employees.get_salary_difference(20000)
# employees.is_current_employee()
# employees.employee_maximum_salary(10010)
# employees.employee_salary_display()
employees.salary_per_title()

