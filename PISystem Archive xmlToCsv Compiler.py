import pandas as pd
from glob import glob
import xml.etree.ElementTree as ET

#Lendo arquivos do ARCHIVE
path_archss = r'ENTER\PATH\HERE\*.xml' #ENTER PATH HERE
archive = sorted(glob(path_archss))

cols = ["IPHost", "IPAddress","UTCSeconds", "LocalDate","Domain", "NameOSUser","ExportFileName", "RecordCount", "AuditFileName", "CreationDate", "Mask","AuditRecordID", "UserID","UTCSecondsPITime", "LocalDatePITime", "Action", "PointID","UTCSecondsTimeStamp", "LocalDateTimeStamp", "TypeBeforeValue", "TypeAfterValue", "TypeBeforeFlags", "TypeAfterFlags", "TypeBeforeStatus", "StateSetID", "DigitalStateCode","Document"]
rows = []

for i in archive:
    root = ET.parse(i).getroot()
    nspiaudit = {'ns': "xml.osisoft.com-schemas-piaudit"}

    for j in root.findall('ns:AuditRecords/ns:AuditRecord', nspiaudit):

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
        action = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue', nspiaudit).attrib['Action']

        ''####PIPoint
        pointid = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue/ns:PIPoint', nspiaudit).attrib['PointID']

        ''#####TimeStamp
        timestamputcseconds = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue/ns:PIValue/ns:TimeStamp', nspiaudit).attrib['UTCSeconds']
        timestamplocaldate = j.find('ns:PITimeSeriesDB/ns:PIArchive/ns:PointValue/ns:PIValue/ns:TimeStamp', nspiaudit).attrib['LocalDate']

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
                    "NameOSUser": nameosuser,
                    "ExportFileName": exportfilename,
                    "RecordCount": recordcount,
                    "AuditFileName": auditfilename,
                    "CreationDate": creationdate,
                    "Mask": mask,
                    "AuditRecordID": auditrecordid,
                    "UserID": userid,
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
                    
df = pd.DataFrame(rows, columns = cols)
df.to_csv('nameOfOutout.csv') #name of outputcsv