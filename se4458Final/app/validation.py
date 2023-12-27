from dotenv import load_dotenv
import os
import pyodbc

load_dotenv()

server = os.getenv("AZURE_SERVER")
port = 1433
user = os.getenv("AZURE_ID")
password = os.getenv("AZURE_PASSWORD")
database = 'finaldatabase'

# Build connection string
conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server},{port};DATABASE={database};UID={user};PWD={password}"
def conn():
    try:
        # Create a connection
        with pyodbc.connect(conn_str, timeout=15) as conn:
            return conn

    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(sqlstate)
        return f"Error connecting to the database. SQLState: {sqlstate}"
# I will use azure sql
def checkUser(username,password):
    try:
        connection = conn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", username, password)
        result = cursor.fetchone()
        # If there is no user with given username and password, it will return None
        if result:  
            return True
        else:
            return False
    
    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        # Close the database connection
        connection.close()