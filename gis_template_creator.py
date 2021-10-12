import cx_Oracle
import sys
import json

class gis_tamplate_creator(object):
	"""docstring for gis_tamplate_creator"""
	def __init__(self, logger,ConfigData):
		self.logger = logger
		self.ConfigData = ConfigData
		self.conn = self.oracle_db_connection() #it returns the connection estabilshed

	def oracle_db_connection(self):
		#------------ Getting information required to establish the connection ------------------------------------

		user = self.ConfigData["oracle_db_info"]["user"]
		password = self.ConfigData["oracle_db_info"]["password"]
		port = self.ConfigData["oracle_db_info"]["port"]
		host = self.ConfigData["oracle_db_info"]["host"]
		service_name = self.ConfigData["oracle_db_info"]["service_name"]
		
		#-----------------------------------------------------------------------------------------------------------

		dsn = cx_Oracle.makedsn(host, port, service_name) 

		#------------ stablishing the connection with the ORACLE database ------------------------------------------
		try:
			connection = cx_Oracle.connect(user=user, password=password, dsn=dsn, encoding="UTF-8")
			self.logger.debug("!!!!!! Connected to Oracle DB !!!!!!!")
		except Exception as e:
			self.logger.error("Error trying to connect to oracle database. %s. %s" %(sys.exc_info()[0],e))
			raise
		#-----------------------------------------------------------------------------------------------------------
		return connection


	def gis_amplifiers(self):
		amplifiers = []
		query = "SELECT AMPLIFIER_ID, LONGITUDE, LATITUDE, PARENT_NODE_ID FROM PNM_EXPORT_AMPLIFIERS"
		try:
			with self.conn.cursor() as cursor:
				for row in cursor.execute(query):
					amplifiers.append({
						"cpeid": row[0],
						"metadata.address": "",
						"metadata.coordinates": "["+str(row[1])+","+str(row[2])+"]",
						"metadata.node": row[3],
						"action":""
					})
		except Exception as e:
			self.logger.error("Error getting the amplifiers information. %s. %s" %(sys.exc_info()[0],e))
			raise
		return amplifiers
				

	def gis_nodes(self):
		nodes = []
		query = "SELECT NODE_ID, LONGITUDE, LATITUDE FROM PNM_EXPORT_NODES"
		try:
			with self.conn.cursor() as cursor:
				for row in cursor.execute(query):
					nodes.append({
						"cpeid": row[0],
						"metadata.address": "",
						"metadata.coordinates": "["+str(row[1])+","+str(row[2])+"]",
					})
		except Exception as e:
			self.logger.error("Error getting the nodes information. %s. %s" %(sys.exc_info()[0],e))
			raise
		return nodes


	def gis_taps(self):
		taps = []
		query = "SELECT TAP_ID, LONGITUDE, LATITUDE, PARENT_NODE_ID, PORTS_NUMBER FROM PNM_EXPORT_TAPS"
		try:
			with self.conn.cursor() as cursor:
				for row in cursor.execute(query):
					taps.append({
						"cpeid": row[3]+row[0],
						"metadata.address": "",
						"metadata.coordinates": "["+str(row[1])+","+str(row[2])+"]",
						"metadata.node": row[3],
						"metadata.capacity": str(row[4]),
						"action": ""                 
					})
		except Exception as e:
			self.logger.error("Error getting the taps information. %s. %s" %(sys.exc_info()[0],e))
			raise
		return taps


	def gis_coverages(self):
		coverages = []
		query = "SELECT NODE_ID, LONGITUDE, LATITUDE, POINT_ORDER FROM PNM_EXPORT_COVERAGES order by NODE_ID, POINT_ORDER DESC"
		try:
			with self.conn.cursor() as cursor:
				coordinates = ""
				for row in cursor.execute(query):
					# the coordinates are concatenated inversely to have the correct order (ascendent)
					coordinates = "["+str(row[1])+","+str(row[2])+"]," + coordinates

					# the conditional means that is the last coordinate of the cable.
					if row[3] == 0:
						coordinates = coordinates.rstrip(',') #delete the last character: ","
						coordinates = "[" + coordinates + "]"
						coverages.append({
							"cpeid": row[0],
							"metadata.coordinates": coordinates #receive the points in json format.
						})
						coordinates = ""			
		except Exception as e:
			self.logger.error("Error getting the coverages information. %s. %s" %(sys.exc_info()[0],e))
			raise
		return coverages


	def gis_cables(self):
		cables = []
		# This query brings the cables information ordered by CABLE_ID and also by POINT_ORDER in a descendant way.
		# The reason is to know the number of coordinates that the cable has at the first iteration of the loop.
		query = "SELECT CABLE_ID, LONGITUDE, LATITUDE, PARENT_NODE_ID, CABLE_DISTANCE, POINT_ORDER FROM PNM_EXPORT_CABLES order by CABLE_ID, POINT_ORDER DESC"
		try:
			with self.conn.cursor() as cursor:
				coordinates = ""
				for row in cursor.execute(query):
					# the coordinates are concatenated inversely to have the correct order (ascendent)
					coordinates = "["+str(row[1])+","+str(row[2])+"]," + coordinates

					# the conditional means that is the last coordinate of the cable.
					if row[5] == 0:
						coordinates = coordinates.rstrip(',') #delete the last character: ","
						coordinates = "[" + coordinates + "]"
						cables.append({ # we add the cable information to the dictionary
							"cpeid": row[0],
							"metadata.address": "",
							"metadata.coordinates": coordinates,
							"metadata.node": row[3],
							"metadata.distance": str(row[4]),
							"action": ""
						})
						coordinates = ""			
		except Exception as e:
			self.logger.error("Error getting the cables information. %s. %s" %(sys.exc_info()[0],e))
			raise
		return cables