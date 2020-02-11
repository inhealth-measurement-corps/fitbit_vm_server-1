import pyodbc

testflag = False
writeflag = True
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
if testflag:
	server = '192.168.0.105' 
	database = 'AnthonyTest' 
	username = 'sa' 
	password = 'fitbitter123' 

else:
	server = r"jhbcru-vsql2\jhbcru_vsql2"
	database = r'mmcfitbit'
	username = r"WIN\zxu67"
	password = r'!+Xz1991'

print(server)
print(username)

connection_str = (
	r'DRIVER={ODBC Driver 13 for SQL Server};'
	r'SERVER='+server+';'
	r'DATABASE='+database+';'
	r'TRUSTED_CONNECTION=yes;'
	r'UID='+username+';'
	r'PWD='+ password
	)

cnxn = pyodbc.connect(connection_str)
cursor = cnxn.cursor()

if writeflag:
	# cursor.execute("INSERT INTO TestTable1 (test1, test2, test3, test4) VALUES (22222, 2, 2, 2)")
	cursor.execute(r"INSERT INTO dbo.PC_Checkin (user_id, checked_in, type, added_on) VALUES (2, CONVERT(datetime,'2019-03-21 00:00:01'), 4, CONVERT(datetime,'2019-03-21 00:00:01')) SELECT * FROM dbo.PC_Checkin")
	cursor.commit()
else:
	cursor.execute("SELECT * FROM dbo.PC_Checkin") 

	row = cursor.fetchone() 
	print("%s \t %s \t %s \t %s \t %s" % ("id", "patient_id", "checked_in", "type", "added_on"))

	while row: 
	    print("%s \t %s \t %s \t %s \t %s" % (row[0], row[1], row[2], row[3], row[4]))  
	    row = cursor.fetchone()
