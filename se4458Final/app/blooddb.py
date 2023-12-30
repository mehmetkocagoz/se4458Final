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

def requestBloodFromDatabase(requestor, blood_type, city, town, email, units, duration):
    connection = conn()
    cursor = connection.cursor()
    # First we will check BloodDonations table, if there is enough blood we will directly send email to requestor 'Blood Found Donor= {'donor_name'}'
    cursor.execute("""
            SELECT SUM(units) FROM BloodDonations WHERE blood_type = ?
        """, (blood_type,))
    total_units_available = cursor.fetchone()[0] or 0
    # If there is enough available units, we will try to collect blood from donors
    # It can be one or more donors therefore I used while loop inside this if clause
    if total_units_available >= units:    
        cursor.execute("""
                    SELECT * FROM BloodDonations WHERE blood_type = ?
                       """,(blood_type,))
        donors = cursor.fetchall()
        blood_need = units
        i=0
        donor_name_list = []
        while (blood_need>0):
            don_ID = donors[i][0]
            donor_name = donors[i][1]
            blood_type = donors[i][2]
            unit = donors[i][3]
            i = i+1
            # If donor donated more then requested units of blood, we will update donor's unit and set the blood_need to 0, loop will end
            if unit > blood_need:
                unit -=blood_need
                blood_need = 0
                cursor.execute("""
                            UPDATE BloodDonations SET units = ? WHERE donation_id = ?;
                               """,(unit,don_ID,))
                donor_name_list.append(donor_name)
            # If donor donated equal request, we will delete donor row and set the blood_need to 0, loop will end
            elif unit == blood_need:
                blood_need = 0
                cursor.execute("""
                            DELETE FROM BloodDonations WHERE donation_id = ?
                               """,(don_ID,))               
                donor_name_list.append(donor_name)
            # Else we will try to collect requested blood units from donors, loop will continue
            else:
                blood_need = blood_need - unit
                cursor.execute("""
                            DELETE FROM BloodDonations WHERE donation_id = ?
                               """,(don_ID,))
                donor_name_list.append(donor_name)
        connection.commit()
    # Else there is no enough blood, we will send a message to queue, queue will handled with another service
    else:
        return "Not enough blood, it sends to queue"
            
    connection.commit()
    connection.close()
    return donor_name_list