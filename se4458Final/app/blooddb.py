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
    
def addBloodToDatabase(donor_name,blood_type,unit):
    connection = conn()
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO BloodDonations (donor_name, blood_type, units) VALUES (?, ?, ?)",
                   (donor_name, blood_type, unit))
    
    connection.commit()
    connection.close()

    return "Blood Added Succesfully"


def createDonorInDatabase(donor_name, blood_type, city, town, email, phone):
    connection = conn()
    cursor = connection.cursor()
    cursor.execute("""
            INSERT INTO Donors (donor_name, blood_type, city, town, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (donor_name, blood_type, city, town, email, phone))
    connection.commit()
    connection.close()
    return "Donor Created Succesfully"