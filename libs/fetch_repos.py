import os

def ssl_server_trust_prompt( trust_dict ):
	return True, 0, True

def pre_build_fetch(opts):
	import git
	if os.path.exists("MaNGOS"):
		print ("Updating MaNGOS sourcecode")
		git.Git('MaNGOS').pull('-u')
	else:
		print ("MaNGOS is not present; checking out MaNGOS")
		git.Git('.').clone('git://github.com/mangos/mangos.git','MaNGOS')
	if os.path.exists("MaNGOS/src/bindings/ScriptDev2"):
		print ("Updating ScriptDev2 sourcecode")
		git.Git('MaNGOS/src/bindings/ScriptDev2').pull('-u');
	else:
		print ("ScriptDev2 is not present; checking out ScriptDev2")
		git.Git('MaNGOS/src/bindings').clone('git://github.com/scriptdev2/scriptdev2.git','ScriptDev2');
		if os.name != "nt": git.Git('MaNGOS').apply('src/bindings/ScriptDev2/patches/'+opts.sd2_patch)


def post_build_fetch():
	import pysvn
	svn_client = pysvn.Client()
	svn_client.callback_ssl_server_trust_prompt = ssl_server_trust_prompt
	#print "current dir: "+os.getcwd()
	if os.path.exists("sd2-acid"):
		print ("Updating ACID sourcecode")
		svn_client.update('./sd2-acid')
	else:
		print ("ACID is not present; checking out ACID")
		svn_client.checkout('https://sd2-acid.svn.sourceforge.net/svnroot/sd2-acid/trunk', './sd2-acid')

	if os.path.exists("unifieddb"):
		print ("Updating UDB sourcecode")
		svn_client.update('./unifieddb')
	else:
		print ("UDB is not present; checking out UDB")
		svn_client.checkout('https://unifieddb.svn.sourceforge.net/svnroot/unifieddb/trunk', './unifieddb')
