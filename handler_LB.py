from logger_class import logger_class
from gis_template_creator import gis_tamplate_creator
import sys
import json
from time import time
import csv
import os

root_path = "/home/porgoa/load_gis"


def check_dir(dir_path):
    if os.path.isdir(dir_path):
        return True
    else:
        return False


# Permision Values permited by the function: [r,w,x]
def check_permission(path, permision):
    res = False
    if permision == 'r':
        res = os.access(path, os.R_OK)
    elif permision == 'w':
        res = os.access(path, os.W_OK)
    elif permision == 'x':
        res = os.access(path, os.X_OK)
    #print("permiso de %s: %s" %(permision,res))
    return res


# the function opens the config JSON file
def Open_Config_Data():
	try:
	    with open(root_path+"/config_file.json","r") as jsonfile:
	        ConfigData = json.load(jsonfile)
	except Exception as e:
	    logger.error("There was an error trying to open the config JSON file. %s. %s" %(sys.exc_info()[0],e))
	    raise
	return ConfigData


def Export_to_csv_file(output_path, List_Records):
	try:
		with open(output_path,'w') as out_fd:
			csv_writer = csv.DictWriter(out_fd, fieldnames = List_Records[0].keys())
			csv_writer.writeheader()
			for record in List_Records:
				csv_writer.writerow(record)
	except Exception as e:
		logger.error("It was not possible to export the csv file (%s). %s, %s" %(output_path.split("/")[-1],sys.exc_info()[0],e))
		raise


def main():
	ConfigData = Open_Config_Data()

	#instantiate the class gis_template_creator.
	gis_instance = gis_tamplate_creator(logger,ConfigData)

	for Elemento in ConfigData["gis_config"]:
		state = ConfigData["gis_config"][Elemento]["state"]
		output_path = ConfigData["gis_config"][Elemento]["output_path"]
		filename = ConfigData["gis_config"][Elemento]["csv_file_name"]
		
		# Check if the Source directory exists for the element
		if not check_dir(output_path):
			logger.error("%s not created and exported: The output directory not found in %s" %(Elemento,output_path)) 
			continue

		# Check if the Output directory is rewritable
		if not check_permission(output_path, 'w'):
			logger.error("%s not created and exported: The Output directory does not have writing permission [%s]" %(Elemento,output_path))
			continue
		
		try:
			if Elemento == "Amplifiers":
				if state == "True":
					template = gis_instance.gis_amplifiers()
					Export_to_csv_file(output_path+"/"+filename, template)
					logger.info("file %s was exported successfully [%s]"%(filename,output_path))
				else:
					logger.info("file %s disabled"%filename)
					continue
			if Elemento == "Nodes":
				if state == "True":
					template = gis_instance.gis_nodes()
					Export_to_csv_file(output_path+"/"+filename, template)
					logger.info("file %s was exported successfully [%s]"%(filename,output_path))
				else:
					logger.info("file %s disabled"%filename)
					continue
			if Elemento == "Taps":
				if state == "True":
					template = gis_instance.gis_taps()
					Export_to_csv_file(output_path+"/"+filename, template)
					logger.info("file %s was exported successfully [%s]"%(filename,output_path))
				else:
					logger.info("file %s disabled"%filename)
					continue
			if Elemento == "Covers":
				if state == "True":
					template = gis_instance.gis_coverages()
					Export_to_csv_file(output_path+"/"+filename, template)
					logger.info("file %s was exported successfully [%s]"%(filename,output_path))
				else:
					logger.info("file %s disabled"%filename)
					continue
			if Elemento == "Cables":
				if state == "True":
					template = gis_instance.gis_cables()
					Export_to_csv_file(output_path+"/"+filename, template)
					logger.info("file %s was exported successfully [%s]"%(filename,output_path))
				else:
					logger.info("file %s disabled"%filename)
					continue
		except Exception as e:
			logger.error("Error creating the file: %s. %s, %s" %(filename,sys.exc_info()[0],e))


if __name__ == "__main__":
	#----- triggering the logs ------
	log = logger_class(root_path)
	logger = log.logger
	#--------------------------------
	main()