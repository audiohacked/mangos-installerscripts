#!/usr/bin/python
import	os, sys, optparse
sys.path.insert( 0, os.path.abspath("libs"))

import dep_check
import fetch_repos
import windows_build
import linux_build

def parse_cmd_args():
	if os.name == "nt":
		install_dir="C:\\MaNGOS"
	else:
		install_dir="/opt/mangos"
	parser = optparse.OptionParser(version="%prog 1.0")
	
	parser.add_option("--mangos-destdir", "--install-dir", "--destdir",
		action="store",
		dest="mangos_destdir",
		default=install_dir)

	parser.add_option("--sd2-patch", "--patch", "--sd2", 
		action="store",
		dest="sd2_patch",
		default="MaNGOS-10938-ScriptDev2.patch")
		
	parser.add_option("--build-dir",
		action="store",
		dest="build_dir",
		default=".")

	parser.add_option("--no-build",
		action="store_false",
	dest="build",
	default=True)

	parser.add_option("--no-install",
		action="store_false",
		dest="install",
		default=True)

	parser.add_option("--no-fetch",
		action="store_false",
	dest="fetch",
	default=True)

	parser.add_option("--no-rebuild",
		action="store_false",
	dest="rebuild",
	default=True)

	parser.add_option("--debug",
		action="store_true",
	dest="debug",
	default=False)

	(options, args) = parser.parse_args()
	return options

if __name__ == '__main__':
	opts = parse_cmd_args()
	if opts.debug: print "Src Build Dir:", opts.build_dir
	if opts.build_dir == ".":
		opts.build_dir = os.getcwd()
	else:
		os.chdir(opts.build_dir)

	if os.name == "nt":
		dep_check.win32()
	else:
		dep_check.linux()

	if opts.fetch: fetch_repos.pre_build_fetch(opts)
	if os.name == "nt":
		if opts.build: windows_build.make()
		if opts.install: windows_build.install(opts)
	else:
		if opts.build: linux_build.make(opts)
	os.chdir(opts.build_dir)
	if opts.fetch: fetch_repos.post_build_fetch()

