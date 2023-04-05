import pyodbc
import pandas as pd
import time
t1 = time.time()

server = 'EMC105608' #write server
database = 'testE' #write base
username = 'myusername' #write username
password = 'secretword' #write password


#IN THIS CASE I HAVE CONNECTED TO A LOCAL DATABASE BUT IT'S POSSIBLE TO CONNECT IN A CLOUD DATABASE. YOU JUST HAVE TO SETTLE THE PARAMETERS CORRECTLY. BELOW YOU CAN CHECK THE LINK OF THE DOCUMENTION OF CONNECTION PROPERTY
#https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=No; fast_executemany=True')
cursor = cnxn.cursor()
print("THE CONNECTION WAS SETTLED!")


#READING THE SPREADSHEET - ENTER THE EXCEL DOCUMENT
df = pd.read_excel('mySweetExcelFile.xlsx', sheet_name = 'TabIWannaWork')

#SETTLING COLUMNS
df['TAG'] = df.TAG.astype('str')
df['TIMESTAMP'] = df.TIMESTAMP.astype('str')
df['VALUE'] = df.VALUE.astype('str')

#LOOP
for i in range(len(df['TAG'])):
    tag = df.loc[i, 'TAG']
    timestamp = df.loc[i, 'TIMESTAMP']
    value = df.loc[i, 'VALUE']
 
    script = '''insert into MYTABLE ([columns1], [column2], [column3]) values ('''
    data = "'" + tag + "','" + timestamp + "','" + value + "')"        

    query = script + data      
    cursor.execute(query)
    cursor.commit()


tempoExec = time.time() - t1
print("Execution Time: {} seconds".format(tempoExec))
