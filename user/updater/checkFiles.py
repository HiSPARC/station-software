import os
import re
import ctypes

# check if you are in admin mode
def checkIfAdmin():
	try:
		is_admin = os.getuid() == 0
	except:
		is_admin = ctypes.windll.shell32.IsUserAnAdmin()

	print is_admin
	return is_admin


# parses something_v19.exe to 19, and something_v20.124.exe to (20, 124).
def parseVersion(filename):
	mo = re.search("_v(\d+)(\.(\d+))?\.exe$", filename)
	if mo:
		return (mo.group(3) == None) and int(mo.group(1)) or (int(mo.group(1)), int(mo.group(3)))

	

def checkIfNewerFileExists(location, searchName, currentVersion):
	fileList = os.listdir(location)
	found = False
	versionFound = 0
	fileFound = ""
	
	print "currentVersion is: %s" % currentVersion
	
	for item in fileList:
		versionNr = parseVersion(item)

		if (item[0:12] == searchName) and (versionNr > currentVersion) and (versionNr > versionFound):
			print "item: %s" % item
			versionFound = versionNr
			fileFound = item
			found = True
	
	return found, fileFound 
	
	
def checkIfEqualFileExists(location, searchName):
	return os.access("%s\%s" % (location, searchName), os.F_OK)