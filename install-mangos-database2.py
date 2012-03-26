#!/usr/bin/python
import re, os, sys, subprocess
import optparse
import zipfile
sys.path.insert( 0, os.path.abspath("libs"))

import dep_check

baselist_unifieddb = (
	'./unifieddb/Full_DB/ForCleanInstallOnly/create_mysql.sql',
	'./unifieddb/Full_DB/ForCleanInstallOnly/scriptdev2_create_mysql.sql',)

baselist_scriptdev2 = (
	'./MaNGOS/src/bindings/ScripDev2/sql/scriptdev2_create_structure_mysql.sql',
	'./MaNGOS/src/bindings/ScripDev2/sql/scriptdev2_script_full.sql',)

baselist_last = (
	'./MaNGOS/sql/characters.sql',
	'./MaNGOS/sql/realmd.sql',)

def base_dbs(args, fresh=True):
	if fresh:
		for sql in baselist_unifieddb:
			execute_sql_file(args, None, sql)

	dlist = ('mangos','scriptdev2','realm','characters')
	for db in dlist: 
		loop_unifieddb(args, database=db);
		loop_mangos(args, database=db);
		loop_acid(args, database=db);
		loop_scriptdev2(args, database=db);

	if fresh:
		for sql in baselist_last:
			execute_sql_file(args, None, sql)
	
def loop_mangos(args, database, fresh=False):
	""" ./MaNGOS/sql/updates/<revision>_<patchorder>_<db>_<string>.sql
	"""
	update_loc = ('./MaNGOS/sql/updates/',)

def loop_scriptdev2(args, database, fresh=False):
	""" ./MaNGOS/src/bindings/ScriptDev2/sql/updates/r<revision>_<db>.sql
	"""
	if fresh:
		for sql in baselist_scriptdev2:
			execute_sql_file(args, database, sql)
	loc = './MaNGOS/src/bindings/ScriptDev2/sql/'
	p = find_latest_update_dir(loc, 'updates')
	s = check_sqlfile_db(p, '^'+database+'_')

def loop_acid(args, database, fresh=False):
	""" ./sd2-acid/<expansion>/<version>/<version>_acid.sql
	    ./sd2-acid/<expansion>/<version>/Service\ Release/<version>_acid.sql
	"""
	update_loc = ('./sd2-acid/',)

def loop_unifieddb(args, database, fresh=False):
	""" ./unifieddb/Updates/<version>_additions/<revision>_corepatch_<db>_<start_rev>_to_<stop_rev>.sql
	    ./unifieddb/Updates/<version>_additions/<revision>_updatepack_<db>.sql
	"""
	""" Search for updates """
	loc = './unifieddb/Updates/'
	p = find_latest_update_dir(loc, '_additions')
	s = check_sqlfile_db(p, '^'+database+'_')
	#execute_sql_file(args, database, s)

def find_latest_update_dir(location, search_string):
	for name in os.listdir(location):
		d = os.path.join(location,name)
		if os.path.isdir(d) and re.search(search_string, d):
			return d
	
def check_sqlfile_db(path, search_string):
	for name in os.listdir(path):
		s = os.path.join(path, name)
		if os.path.isfile(s) and re.match(search_string, s):
			print s

def extract_sql_files(dbquery, args):
	if dbquery['zipfile'] != None and not args.testing:
		print "Extracting zip: "+os.path.dirname(exec_tree+dbquery['sqlfile'])+"/"+dbquery['zipfile']
		home = os.getcwd()
		os.chdir(os.path.dirname(exec_tree+dbquery['sqlfile']))
		zf = zipfile.ZipFile(dbquery['zipfile'])
		zf.extract(os.path.basename(dbquery['sqlfile']))
		os.chdir(home)

def execute_sql_file(args, database, sql):
	execute_str = "mysql -u "+args.username+args.cmd_passwd_str+" "+database+" < "+sql
	if os.path.splitext(sql) != '.sql': pass	
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
	if os.name == "nt":
		dep_check.win32()
	else:
		dep_check.linux()

	base_dbs(my_args, my_args.update)

