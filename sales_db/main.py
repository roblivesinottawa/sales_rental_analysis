from connect import make_connection

def main():
    '''This function establishes a connection to the database'''
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    print(cursor.fetchall())
    cursor.close()
    conn.close()

def create_database():
    '''This function creates a database'''
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS Sales")
    print("DATABASE CREATED SUCCESSFULLY.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
    create_database()


