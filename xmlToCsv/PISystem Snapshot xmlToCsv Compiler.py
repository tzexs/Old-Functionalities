import pandas as pd
from glob import glob
import xml.etree.ElementTree as ET

#Lendo arquivos do snapshot
path_snp = r'ENTER\PATH\HERE\*.xml' #ENTER PATH HERE
snapshot = sorted(glob(path_snp))

cols = ["IPHost", "IPAddress","UTCSeconds", "LocalDate","Domain", "NameOUser","ExportFileName", "RecordCount", "AuditFileName", "CreationDate", "Mask","AuditRecordID", "UserID","Name","UTCSecondsPITime", "LocalDatePITime", "Action", "PointID","UTCSecondsTimeStamp", "LocalDateTimeStamp", "TypeBeforeValue", "TypeAfterValue", "TypeBeforeFlags", "TypeAfterFlags", "TypeBeforeStatus", "StateSetID", "DigitalStateCode","Document"]
rows = []

for i in snapshot:
    root = ET.parse(i).getroot()
    nspiaudit = {'ns': "xml.osisoft.com-schemas-piaudit"}

    for j in root.findall('ns:AuditRecords/ns:AuditRecord', nspiaudit):

        name = j.find('ns:PIUser', nspiaudit).attrib['Name']
        
        if "SS-TR0" in name:
             
            ''#PIServer
            iphost = root[0].get('IPHost')
            ipadress = root[0].get('IPAddress')

            ''#ExportDate
            utcseconds = root[1].get('UTCSeconds')
            localdate = root[1].get('LocalDate')

            ''#OSUser
            domain = root[2].get('Domain')
            nameosuser = root[2].get('Name')

            ''#AuditRecords
            exportfilename = root[3].get('ExportFileName')
            recordcount = root[3].get('RecordCount')
            auditfilename = root[3].get('AuditFileName')
            creationdate = root[3].get('CreationDate')
            mask = root[3].get('Mask')      

            ''#AuditRecordID
            auditrecordid = j.get('AuditRecordID')

            ''##PIUser
            userid = j.find('ns:PIUser', nspiaudit).attrib['UserID']
    

            ''##PITime
            pitimeutcseconds = j.find('ns:PITime', nspiaudit).attrib['UTCSeconds']
            pitimelocaldate = j.find('ns:PITime', nspiaudit).attrib['LocalDate']

            ''###PointValue
            try:
                action = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue', nspiaudit).attrib['Action']
            except AttributeError:
                action = str("")


            ''####PIPoint
            try:
                pointid = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue/ns:PIPoint', nspiaudit).attrib['PointID']
            except:
                pointid = str("")

            ''#####TimeStamp
            try:
                timestamputcseconds = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue/ns:PIValue/ns:TimeStamp', nspiaudit).attrib['UTCSeconds']
            except:
                timestamputcseconds = str("")

            try:
                timestamplocaldate = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue/ns:PIValue/ns:TimeStamp', nspiaudit).attrib['LocalDate']
            except:
                timestamplocaldate = str("")


            ''######Value
            try:
                typebeforevalue = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue/ns:PIValue/ns:Value/ns:Before', nspiaudit).attrib['Type']
            except AttributeError:
                typebeforevalue = str("")

            try:
                typeaftervalue = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue/ns:PIValue/ns:Value/ns:After', nspiaudit).attrib['Type']
            except AttributeError:
                typeaftervalue = str("")


            ''######Flags
            try: 
                typebeforeflags = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue/ns:PIValue/ns:Flags/ns:Before', nspiaudit).attrib['Type']
            except AttributeError:
                typebeforeflags = str("")

            try:
                typeafterflags = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue/ns:PIValue/ns:Flags/ns:After', nspiaudit).attrib['Type']
            except AttributeError:
                typeafterflags = str("")
                
        
            ''######Before-Status
            try:
                typebeforestatus = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue/ns:PIValue/ns:Status/ns:Before', nspiaudit).attrib['Type']
            except AttributeError:
                typebeforestatus = str("")

            try:
                statesetid = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue/ns:PIValue/ns:Status/ns:Before', nspiaudit).attrib['StateSetID']
            except AttributeError:
                statesetid = str("")

            try:
                digitalstadecode = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue/ns:PIValue/ns:Status/ns:Before', nspiaudit).attrib['DigitalStateCode']
            except AttributeError:
                digitalstadecode = str("")

        #Adicionar linhas

            rows.append({"IPHost":iphost,
                    "IPAddress": ipadress,
                    "UTCSeconds": utcseconds,
                    "LocalDate": localdate,
                    "Domain": domain,
                    "Name": name,
                    "ExportFileName": exportfilename,
                    "RecordCount": recordcount,
                    "AuditFileName": auditfilename,
                    "CreationDate": creationdate,
                    "Mask": mask,
                    "AuditRecordID": auditrecordid,
                    "UserID": userid,
                    "Name": name,
                    "UTCSeconds": pitimeutcseconds,
                    "LocalDate": pitimelocaldate,
                    "Action": action,
                    "PointID": pointid,
                    "UTCSecondsTimeStamp": timestamputcseconds, 
                    "LocalDateTimeStamp": timestamplocaldate, 
                    "TypeBeforeValue": typebeforevalue,
                    "TypeAfterValue": typeaftervalue,
                    "TypeBeforeFlags": typebeforeflags, 
                    "TypeAfterFlags": typeafterflags,
                    "TypeBeforeStatus": typebeforestatus, 
                    "StateSetID": statesetid, 
                    "DigitalStateCode": digitalstadecode,
                    "Document": i
                    })
        else:
            pass


df = pd.DataFrame(rows, columns = cols)
df.to_csv('nameOfOutout.csv') #name of outputcsv
