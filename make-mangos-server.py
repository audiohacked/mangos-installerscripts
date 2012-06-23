#!/usr/bin/python
import	os, sys
sys.path.insert( 0, os.path.abspath("libs"))

import dep_check
import fetch_repos
import windows_build
import linux_build

import argparse
def parse_cmd_args():
	if os.name == "nt":
		install_dir="C:\\MaNGOS"
	else:
		install_dir="/opt/mangos"

	parser = argparse.ArgumentParser(description='Build MaNGOS Server python script')
	parser.add_argument("--mangos-destdir", "--install-dir", "--destdir",
		default=install_dir)

	parser.add_argument("--sd2-patch", "--patch", "--sd2", 
		default="MaNGOS-11167-ScriptDev2.patch")
		
	parser.add_argument("--build-dir",
		default=".")

	parser.add_argument("--no-build",
		action="store_false",
		dest="build")

	parser.add_argument("--no-install",
		action="store_false",
		dest="install")

	parser.add_argument("--no-fetch",
		action="store_false",
		dest="fetch")

	parser.add_argument("--no-post-fetch",
		action="store_false",
		dest="post_fetch")

	parser.add_argument("--no-rebuild",
		action="store_false",
		dest="rebuild")

	parser.add_argument("--no-patch",
		action="store_false",
		dest="patch")

	parser.add_argument("--debug",
		action="store_true",
		dest="debug")
	
	return parser.parse_args()

if __name__ == '__main__':
	opts = parse_cmd_args()

	if opts.debug: print ("Src Build Dir: "+ opts.build_dir)
	if opts.build_dir == ".":
		opts.build_dir = os.getcwd()
	else:
		os.chdir(opts.build_dir)
	if opts.debug: print ("Dep Check!!!!")
	if os.name == "nt":
		dep_check.win32(opts)
	else:
		dep_check.linux(opts)

	if opts.debug: print ("Fetching Pre-Build")
	if opts.fetch: fetch_repos.pre_build_fetch(opts)

	if opts.debug: print ("Building Server")
	if os.name == "nt":
		if opts.build: windows_build.make(opts)
		if opts.install: windows_build.install(opts)
	else:
		if opts.build: linux_build.make(opts)
	os.chdir(opts.build_dir)

	if opts.debug: print ("Fetching Post-Build")
	if opts.post_fetch: fetch_repos.post_build_fetch(opts)

