import cx_Oracle
import sys

user = "pnm"
password = "$PNM2021"

port = "1521"
host_production = "tigotvgisdb.telecel.net.py"
host_developer = "10.16.202.49"
db_production = "PYGP"
db_developer = "PYGD"

dsn_d = cx_Oracle.makedsn(host_developer,port,db_developer)
dsn_p = cx_Oracle.makedsn(host_production,port,db_production)

print("dsn_d:", dsn_d)
#print("dsn_p:", dsn_p)

try:
	connection = cx_Oracle.connect(user=user, password=password, dsn=dsn_d, encoding="UTF-8")
	print("!!!!!! Connected to Oracle DB !!!!!!!")
	print("--------------")
except Exception as e:
	raise
	print(sys.exc_info()[0],e)

cursor = connection.cursor()

with connection.cursor() as cursor:
	for row in cursor.execute("SELECT * FROM PNM_EXPORT_TAPS where rownum <= 10"):
		print(row)

print("------------------------------------------------------------------------------------")

with connection.cursor() as cursor:
	for row in cursor.execute("SELECT * FROM PNM_EXPORT_AMPLIFIERS where rownum <= 10"):
		print(row)

print("------------------------------------------------------------------------------------")

with connection.cursor() as cursor:
	for row in cursor.execute("SELECT LATITUDE, AMPLIFIER_ID FROM PNM_EXPORT_AMPLIFIERS where rownum <= 10"):
		print(row)
		print(row[0])