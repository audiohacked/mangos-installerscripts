#!/usr/bin/python
import re, os, sys, subprocess
import optparse
import _mysql
import zipfile
sys.path.insert( 0, os.path.abspath("libs"))

import dep_check

mangos_dbversion_str = {'characters':'character_db_version',
			'mangos':'db_version',
			'realmd':'realmd_db_version',
			'scriptdev2':'sd2_db_version'}

def base_dbs(args, fresh=False):
	if fresh:
		dlist = ('mangos','scriptdev2','realm','characters')
		flist = ('./unifieddb/Full_DB/ForCleanInstallOnly/create_mysql.sql',
			'./unifieddb/Full_DB/ForCleanInstallOnly/scriptdev2_create_mysql.sql',
			'./MaNGOS/src/bindings/ScripDev2/sql/scriptdev2_create_structure_mysql.sql',
			'./MaNGOS/src/bindings/ScripDev2/sql/scriptdev2_script_full.sql')
		nlist = ('./MaNGOS/sql/characters.sql',
			'./MaNGOS/sql/realmd.sql')
	else:
		dlist = ('mangos','scriptdev2','characters')

	for fsql in flist:
				
	for db in dlist: 
		loop_mangos(args, database=db);
		loop_scriptdev2(args, database=db);
		loop_acid(args, database=db);
		loop_unifieddb(args, database=db);
	
def loop_mangos(args, database=None, fresh=False):
	""" ./MaNGOS/sql/updates/<revision>_<patchorder>_<db>_<string>.sql
	"""
	if fresh:
		pass
	else:
		pass

def loop_scriptdev2(args, fresh=False):
	""" ./MaNGOS/src/bindings/ScriptDev2/sql/r<revision>_<db>.sql
	"""
	if fresh:
		pass
	else:
		pass

def loop_acid(args, fresh=False):
	""" ./sd2-acid/<expansion>/<version>/<version>_acid.sql
	    ./sd2-acid/<expansion>/<version>/Service\ Release/<version>_acid.sql
	""" 
	if fresh:
		pass
	else:
		pass

def loop_unifieddb(args, fresh=False):
	""" ./unifieddb/Updates/<version>_additions/<revision>_corepatch_<db>_<start_rev>_to_<stop_rev>.sql
	    ./unifieddb/Updates/<version>_additions/<revision>_updatepack_<db>.sql
	"""
	if fresh:
		pass
	else:
		pass
	
def delete_mangos_dbs(args, full_clean=False):
	conn = _mysql.connect(host="localhost",
			  port=3306,
			  user=args.username,
			  passwd=args.passwd)

	try:
		try:
			print "Dropping Database: mangos"
			conn.query("DROP DATABASE mangos;")
		except _mysql.OperationalError:
			pass
		
		try:
			print "Dropping Database: scriptdev2"
			conn.query("DROP DATABASE scriptdev2;")
		except _mysql.OperationalError:
			pass
		
		if full_clean:
			try:
				print "Dropping Database: characters"
				conn.query("DROP DATABASE characters;")
			except _mysql.OperationalError:
				pass
		
			try:
				print "Dropping Database: realmd"
				conn.query("DROP DATABASE realmd;")
			except _mysql.OperationalError:
				pass
	finally:
		conn.close()

 
def fresh_db_install(args):
	print "Performing a Fresh Install"
	delete_mangos_dbs(args, full_clean=True)
	db_install_list = open(args.filename, 'rU')
	for query in get_sql_entries(db_install_list):
		extract_sql_files(query, args)
		execute_sql_file(query, args)

def update_db_install(args):
	print "Performing an Update Install"
	delete_mangos_dbs(args)
	db_install_list = open(args.filename, 'rU')
	for query in get_sql_entries(db_install_list):
		extract_sql_files(query, args)
		execute_sql_file(query, args)
	
def get_mangos_db_version(args, dbname="characters"):
	  conn = _mysql.connect(host="localhost",
				port=3306,
				user=args.username,
				passwd=args.passwd)
	  conn.query("SHOW COLUMNS FROM "+dbname+"."+mangos_dbversion_str[dbname])
	  result = conn.store_result()
	  print result.fetch_row()[0][0]

def extract_sql_files(dbquery, args):
	if dbquery['dbsrctree'] == "mangos":
		exec_tree = "MaNGOS"
	elif dbquery['dbsrctree'] == "scriptdev2":
		exec_tree = "MaNGOS/src/bindings/ScriptDev2" 
	elif dbquery['dbsrctree'] == "acid":
		exec_tree = "sd2-acid"
	elif dbquery['dbsrctree'] == "udb":
		exec_tree = "unifieddb"
	else:
		exec_tree = "."

	if dbquery['zipfile'] != None and not args.testing:
		print "Extracting zip: "+os.path.dirname(exec_tree+dbquery['sqlfile'])+"/"+dbquery['zipfile']
		home = os.getcwd()
		os.chdir(os.path.dirname(exec_tree+dbquery['sqlfile']))
		zf = zipfile.ZipFile(dbquery['zipfile'])
		zf.extract(os.path.basename(dbquery['sqlfile']))
		os.chdir(home)

def execute_sql_file(dbquery, args):
	if dbquery['dbsrctree'] == "mangos":
		exec_tree = "MaNGOS"
	elif dbquery['dbsrctree'] == "scriptdev2":
		exec_tree = "MaNGOS/src/bindings/ScriptDev2" 
	elif dbquery['dbsrctree'] == "acid":
		exec_tree = "sd2-acid"
	elif dbquery['dbsrctree'] == "udb":
		exec_tree = "unifieddb"
	else:
		exec_tree = "."

	if dbquery['dbname'] == None:
		dbname = ""
	else:
		dbname = " "+dbquery['dbname']

	execute_str = "mysql -u "+args.username+args.cmd_passwd_str+dbname+" < "+exec_tree+dbquery['sqlfile']
	
	if args.testing:
		print execute_str
	else:
		print "Executing: ",execute_str
		try:
			retcode = subprocess.call(execute_str, shell=True)
			if retcode < 0:
				print >>sys.stderr, "Child was terminated by signal", -retcode
			#else:
			#	print >>sys.stderr, "Child returned", retcode
		except OSError, e:
			print >>sys.stderr, "Execution failed:", e
	

def get_sql_entries(db_install_list):
	queries = [] 
	buffer = db_install_list.readlines()
	for line in buffer:
		db_files = match_dbline.match(line)
		if db_files != None:
			queries.append( db_files.groupdict() )
	return queries

def parse_password_callback(option, opt, value, parser):
		parser.values.cmd_passwd_str = " --password="+value
		parser.values.passwd = value

def parse_update_callback(option, opt, value, parser):
		parser.values.update = True
		if parser.values.filename == "fresh.dbinst":
			parser.values.filename = "update.dbinst"
			
def parse_cmd_args():
	parser = optparse.OptionParser(version="%prog 2.0")

	parser.set_defaults(username="mangos", 
						passwd="mangos",
						filename="fresh.dbinst",
						update=False)
	
	parser.add_option("-t", "--test", "--dry-run",
					  action="store_true",
					  dest="testing",
					  default=False)
	
	parser.add_option("-x", "--exec", "--execute",
					  action="store_false",
					  dest="testing",
					  default=False)

	parser.add_option("--up", "--update",
					  action="callback",
					  callback=parse_update_callback,					 
					  dest="update",
					  default=False)
	
	parser.add_option("-p", "--pass", "--password",
					  action="callback",
					  type="string",
					  callback=parse_password_callback,
					  dest="cmd_passwd_str",
					  default=" -p")
	
	parser.add_option("-u", "--user", "--username",
					  action="store",
					  dest="username")
	
	parser.add_option("--db", "--dbfile",
					  action="store",
					  dest="filename")

	(options, args) = parser.parse_args()
	return options

if __name__ == '__main__':
	my_args = parse_cmd_args()
	#print (my_args)
	if os.name == "nt":
		dep_check.win32()
	else:
		dep_check.linux()

	base_dbs(my_args, my_args.update)

