import sys
import webbrowser
try:
	from urllib2 import urlopen
except: # the module has been renamed in Python 3.0
	from urllib.request import urlopen
try:
	from httplib import HTTPConnection, HTTPSConnection, HTTPException, responses
except: # the module has been renamed in Python 3.0
	from http.client import HTTPConnection, HTTPSConnection, HTTPException, responses
try:
	from thread import start_new_thread
except: # the module has been renamed in Python 3.0
	from _thread import start_new_thread
import array
import time
import datetime

#-------------------------------------------------------------------------------------
#--- print header
#-------------------------------------------------------------------------------------
print "\n****************************************************************************"
print "Web Admin Finder"
print "Written by: Sro [http://sro.co.il]"
print "Established on code of Guy Mizrahi's [http://guym.co.il/admin-panel-finder/]"
print "Date: 09 april 2010"
print "Version: 1.0"
print "Description: security tool that help you see your site from hackers eyes"
print "****************************************************************************\n"

#-------------------------------------------------------------------------------------
#--- function error(message)
#-------------------------------------------------------------------------------------
def error(message):
	help()
	print message
	sys.exit()

#-------------------------------------------------------------------------------------
#--- function isset(var)
#-------------------------------------------------------------------------------------
def isset(var):
	if var in locals() or var in globals():
		return True
	else:
		return False

#-------------------------------------------------------------------------------------
#--- function help()
#-------------------------------------------------------------------------------------
def help():
	print "\n--- help -----------------------------------------------------------------------\n"
	print "syntax:\n"
	print "   web-admin-finder.py (site[::ports[::timeout]] | "
	print "   https://site[::ports[::key_file[::cert_file[::strict[::timeout]]]]])"
	print "   (dictionary[::chars]) [dictionary[::chars]] [dictionary[::chars]]"
	print "   [\explorer:open|none] [\print:normal|success|faild|none] [\\threads:number]"
	print "\n\nparameters:"
	print "\n   site (necessary)"
	print "      the site that you want to checking."
	print "      optionally: with the separate :: can you supplement ports and time out."
	print "      example1: somesite.com"
	print "      example2: http://www.somesite.com::80,95,105"
	print "      example2: http://www.somesite.com::80::10"
	print "\n   dictionary (one is necessary)[the remains is optionally]"
	print "      the dictionary path (local file or remote site)."
	print "      optionally: chars for put after every dictionary line."
	print "      example1: directories.txt"
	print "      example2: somesite.com/dictionary.dic::/ dictionary2.dic::.php"
	print "\n   \explorer [optionally]"
	print "      when the software found path, it's open with the default explorer"
	print "      open - open the path found."
	print "      none - not open the path found."
	print "      default: open"
	print "      example1: \explorer:none"
	print "\n   \print [optionally]"
	print "      what print in screen during the scan."
	print "      normal - print all results."
	print "      success - print only good results."
	print "      faild - print only faild results."
	print "      none - no print nothing except report lastly."
	print "      default: normal"
	print "      example1: \print:debug"
	print "\n   \\threads [optionally]"
	print "      for quickly scan, the software can connect and attempt with many threads."
	print "      every thread is connection."
	print "      default: 10"
	print "      example1: \\threads:1"
	print "\n\nexamples:\n"
	print "   web-admin-finder.py www.tk http://guym.co.il/demos/admin_finder/adminpath.txt"
	print "   web-admin-finder.py www.tk dictionary.txt \explorer:none \print:success"
	print "   web-admin-finder.py http://www.tk directories.txt::/ files.txt extensions.txt"
	print "\n--------------------------------------------------------------------------------\n"

#-------------------------------------------------------------------------------------
#--- function checkURL(site, url, ports, SSLkey, SSLcert, SSLstrict, timeout, mode, explorer, debug)
#-------------------------------------------------------------------------------------
def checkURL(site, url, port, SSLkey, SSLcert, SSLstrict, timeout, mode, explorer, debug):
	# counters
	global activeThreads, result
	try:
		if site[:7] == "http://":
			# cut the strint "http://"
			site = site[7:]
			if timeout != -1:
				conn = HTTPConnection(site, port, timeout)
			elif port != -1:
				conn = HTTPConnection(site, port)
			else:
				conn = HTTPConnection(site)
		else:
			# cut the strint "https://"
			site = site[8:]
			if timeout != -1:
				conn = HTTPSConnection(site, port, SSLkey, SSLcert, SSLstrict, timeout)
			elif SSLstrict != -1:
				conn = HTTPSConnection(site, port, SSLkey, SSLcert, SSLstrict)
			elif SSLcert != -1:
				conn = HTTPSConnection(site, port, SSLkey, SSLcert)
			elif SSLkey != -1:
				conn = HTTPSConnection(site, port, SSLkey)
			elif port != -1:
				conn = HTTPSConnection(site, port)
			else:
				conn = HTTPSConnection(site)
		conn.request("GET", url)
		resp = conn.getresponse()
		if resp.status == 404:
			if mode == "normal" or mode == "faild":
				print resp.status, "{" + resp.reason + "}", debug
		else:
			if mode == "normal" or mode == "success":
				print resp.status, "{" + resp.reason + "}", debug
			if explorer == "open":
				webbrowser.open(url)
		result.append(resp.status)
		conn.close()
	except Exception, e:
		print e
	activeThreads -= 1

#-------------------------------------------------------------------------------------
#--- calibration counters
#-------------------------------------------------------------------------------------
# count how many connections running now
activeThreads = 0
# count how many paths we already try
currentPath = 0
# hold result connections, at finish scan it shown report
result = array.array('h')

#-------------------------------------------------------------------------------------
#--- default values of parameters
#-------------------------------------------------------------------------------------
siteArg = "/"
mode = "normal"
explorer = "open"
threads = 10

#-------------------------------------------------------------------------------------
#--- scan parameters
#-------------------------------------------------------------------------------------
for parameter in sys.argv:
	# the first parameter is the path and the name of the file. it's not useful.
	if parameter == sys.argv[0]: continue
	
	if parameter[0] == "\\":
		# split sub parameter from parameter if is there
		if parameter.find(":") > -1:
			parameter = parameter.split(":")
			parameterArg = parameter[1]
			parameter = parameter[0]
		# define settings
		if parameter == "\\print":
			if parameterArg == "normal" or parameterArg == "success" or parameterArg == "faild" or parameterArg == "none":
				mode = parameterArg
			else:
				error("the argument {" + parameterArg + "} of the parameter {" + parameter + "} is invalid!")
		elif parameter == "\\explorer":
			if parameterArg == "open" or parameterArg == "none":
				explorer = parameterArg
			else:
				error("the argument {" + parameterArg + "} of the parameter {" + parameter + "} is invalid!")
		elif parameter == "\\threads":
			if parameterArg.isdigit():
				if parameterArg <= 0:
					error("the argument {" + parameterArg + "} of the parameter {" + parameter + "} must to be at least 1!")
				threads = int(parameterArg)
			else:
				error("the argument {" + parameterArg + "} of the parameter {" + parameter + "} is invalid!")
		else:
			error("the parameter {" + parameter + "} is invalid!")
	else:
		# split sub parameter from parameter if is there
		if isset("site"):
			if parameter.find("::") > -1:
				parameter = parameter.split("::")
				parameterArg = parameter[1]
				parameter = parameter[0]
		# define settings
		if not isset("site"):
			parameter = parameter.split("::")
			if len(parameter) > 0: site = parameter[0]
			else: site = parameter
			if len(parameter) > 1: ports = parameter[1]
			else: ports = -1
			if site[:8] == "https://":
				if len(parameter) > 2: SSLkey = parameter[2]
				else: SSLkey = -1
				if len(parameter) > 3: SSLcert = parameter[3]
				else: SSLcert = -1
				if len(parameter) > 4: SSLstrict = parameter[4]
				else: SSLstrict = -1
				if len(parameter) > 5: timeout = parameter[5]
				else: timeout = -1
			else:
				if len(parameter) > 2: timeout = parameter[2]
				else: timeout = -1
				SSLkey = -1
				SSLcert = -1
				SSLstrict = -1
				if site[:7] != "http://":
					site = "http://" + site
		elif not isset("dic1"):
			dic1 = parameter
			if isset("parameterArg"):
				dic1Arg = parameterArg
		elif not isset("dic2"):
			dic2 = parameter
			if isset("parameterArg"):
				dic2Arg = parameterArg
		elif not isset("dic3"):
			dic3 = parameter
			if isset("parameterArg"):
				dic3Arg = parameterArg
		else:
			error("Error! what is this parameter {" + parameter + "}?")
	# deleting for the next ring
	if isset("parameterArg"):
		del parameterArg

#-------------------------------------------------------------------------------------
#--- quickly review that all is fine
#-------------------------------------------------------------------------------------
# if not there any parameter, print help
if len(sys.argv) == 1:
	error("")

# check if is there a site
if not isset("site"): error("missing site!")

# check if is there a dictionary
if not isset("dic1"): error("missing dictionary!")

# try connect to the site
try: urlopen(site)
except: error("connection to {" + site + "} is failed!")

#-------------------------------------------------------------------------------------
#--- open dictionaries files
#-------------------------------------------------------------------------------------
if isset("dic1"):
	try: directories = open(dic1).read().split("\n")
	except:
		try: directories = urlopen(dic1).read().split("\n")
		except:	error("cannot open the first dictionary")
	paths = len(str(ports).split(",")) * len(directories)
else: # len(blank variable) return 0. needy to whiles
	directories = ""

if isset("dic2"):
	try: files = open(dic2).read().split("\n")
	except:
		try: files = urlopen(dic2).read().split("\n")
		except:	error("cannot open the second dictionary")
	paths = paths * len(files)
else:
	files = ""

if isset("dic3"):
	try: extensions = open(dic3).read().split("\n")
	except:
		try: extensions = urlopen(dic3).read().split("\n")
		except:	error("cannot open the third dictionary")
	paths = paths * len(extensions)
else:
	extensions = ""

#-------------------------------------------------------------------------------------
#--- start scan
#-------------------------------------------------------------------------------------
timeStart = datetime.datetime.now()
timeStartGm = time.gmtime()
print "Testing site:", site
print "Paths to scan:", paths
print "Started at:", time.strftime("%d/%m/%Y %H:%I:%S", timeStartGm)
print "--------------------------------------------------------------------------------"

directoriesLine = 0
while 1:
	filesLine = 0
	while 1:
		extensionsLine = 0
		while 1:
			for port in str(ports).split(","):
				# the strip is for the \r of any lines
				url = siteArg + directories[directoriesLine].strip(None)
				if isset("dic1Arg"): url += dic1Arg
				if isset("dic2"): url += files[filesLine].strip(None)
				if isset("dic2Arg"): url += dic2Arg
				if isset("dic3"): url += extensions[extensionsLine].strip(None)
				if isset("dic3Arg"): url += dic3Arg
				
				while activeThreads >= threads: pass
				activeThreads += 1
				currentPath += 1
				debug = "location: " + str(currentPath) + "/" + str(paths) + " thread: " + str(activeThreads) + "/" + str(threads) + " path: " + url
				port = int(port)
				if port > -1: debug += " port: " + port

				start_new_thread(checkURL, (site, url, port, SSLkey, SSLcert, SSLstrict, timeout, mode, explorer, debug))
			extensionsLine += 1	
			if extensionsLine >= len(extensions): break
		filesLine += 1
		if filesLine >= len(files): break
	directoriesLine += 1
	if directoriesLine >= len(directories): break

#-------------------------------------------------------------------------------------
#--- print report
#-------------------------------------------------------------------------------------
while activeThreads > 0: pass
print "\n--------------------------------------------------------------------------------"
print "REPORT"
print "  CLI command:", " ".join(sys.argv)
print "  Testing site:", site
print "  Started at:", time.strftime("%d/%m/%Y %H:%I:%S", timeStartGm)
print "  Finished at:", time.strftime("%d/%m/%Y %H:%I:%S", time.gmtime())
print "  Scan time:", datetime.datetime.now() - timeStart
print "  Paths that scan:", paths
print "\nRESULT"
print "count code message"

# the array result, contain no' response of the requests, example: 404,404,200,404
# we need to print on every result, how many times it response
# first we create a range: 1,2,3,4....len(result) and put one after the one to x
# second we check if the contain of result[x] is the first presence
# if yes, we print the contain of result[x] (no' response) and how many times it's existing
for x in range(len(result)):
	if result.index(result[x]) == x:
		print "%3s  " % result.count(result[x]), result[x], "", responses[result[x]]

print "\nDONE"
