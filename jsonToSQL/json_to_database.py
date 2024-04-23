import pyodbc
import pandas as pd
from dotenv import load_dotenv
import os
import json

load_dotenv()


#DATABASE CREDENTIALS
db_server = os.getenv("DB_SERVER")
db_name = os.getenv("DB_NAME")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

#IN THIS CASE I HAVE CONNECTED TO A LOCAL DATABASE BUT IT'S POSSIBLE TO CONNECT IN A CLOUD DATABASE. YOU JUST HAVE TO SETTLE THE PARAMETERS CORRECTLY. BELOW YOU CAN CHECK THE LINK OF THE DOCUMENTION OF CONNECTION PROPERTY
#https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+db_server+';DATABASE='+db_name+';UID='+db_username+';PWD='+db_password+';ENCRYPT=No; fast_executemany=True')
cursor = cnxn.cursor()
print("Successfully connected!")

with open("path/file.json", encoding=' utf-8') as my_json:
    data = json.load(my_json)

print(data)
df = pd.DataFrame(data)

#MAPPING COLUMNS / in this demonstration I used just a sample
df['TAG'] = df.TAG.astype('str')
df['TIMESTAMP'] = df.TIMESTAMP.astype('str')
df['VALUE'] = df.VALUE.astype('str')

# START LOOP
for i in range(len(df['TAG'])):
    tag = df.loc[i, 'TAG']
    timestamp = df.loc[i, 'TIMESTAMP']
    value = df.loc[i, 'VALUE']
 
    script = '''insert into MYTABLE ([columns1], [column2], [column3]) values ('''
    data = "'" + tag + "','" + timestamp + "','" + value + "')"        

    query = script + data      
    cursor.execute(query)
    cursor.commit()

