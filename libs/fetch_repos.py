import os, sys

def ssl_server_trust_prompt( trust_dict ):
	return True, 0, True

def git_clone( remote_repo, local_dir=None, new=True ):
	import dulwich.index, dulwich.client, dulwich.repo, urllib
	try:
		client, host_path = dulwich.client.get_transport_and_path(remote_repo)
		if local_dir is None:
			local_dir = host_path.split("/")[-1]
		if new:
			os.mkdir(local_dir)
			r = dulwich.repo.Repo.init(local_dir)
		else:
			r = dulwich.repo.Repo(local_dir)
		remote_refs = client.fetch(host_path, r)
		r['HEAD'] = remote_refs['refs/heads/master']
		dulwich.index.build_index_from_tree(r.path, r.index_path(), r.object_store, r['HEAD'].tree)
	except:
		pass
	finally:
		print("---Sorry! There was a fatal error in cloning!")
		print("---   Please try cloning manually "+remote_repo+" into "+local_dir)

def git_apply( local_repo, patch ):
	import dulwich.index, dulwich.repo, dulwich.patch
	try:
		f = open(patch , "rU")
		commit, diff, version = dulwich.patch.git_am_patch_split(f)
	except:
		pass
	finally:
		print("---Sorry! Unable to auto patch! Please try manually!")

def pre_build_fetch(opts):
	if os.path.exists("mangos.git"):
		print("Updating MaNGOS sourcecode")
		git_clone('git://github.com/mangos/mangos.git', 'mangos.git', new=False)
	else:
		print("MaNGOS is not present; checking out MaNGOS")
		git_clone('git://github.com/mangos/mangos.git', 'mangos.git', new=True)

	if os.path.exists("mangos.git/src/bindings/ScriptDev2"):
		print("Updating ScriptDev2 sourcecode")
		git_clone('git://github.com/scriptdev2/scriptdev2.git', 'mangos.git/src/bindings/ScriptDev2', new=False)
	else:
		print("ScriptDev2 is not present; checking out ScriptDev2")
		git_clone('git://github.com/scriptdev2/scriptdev2.git', 'mangos.git/src/bindings/ScriptDev2')

	if opts.patch and os.name != "nt":
		print("Applying ScriptDev2 Patch for MaNGOS")
		git_apply('mangos.git', 'mangos.git/src/bindings/ScriptDev2/patches/'+opts.sd2_patch)

def post_build_fetch(opts):
	import pysvn
	svn_client = pysvn.Client()
	svn_client.callback_ssl_server_trust_prompt = ssl_server_trust_prompt
	if opts.debug: print ("current dir: "+os.getcwd())
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

