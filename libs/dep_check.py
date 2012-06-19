import os, sys, subprocess

frameworkdir = "C:\\Windows\\Microsoft.NET\\Framework\\"
git_install_dir = 'C:\\Program Files (x86)\\Git'

def win32(opts):
	if os.name == "nt":
		import windows_registry
	else:
		print "You are trying to run the windows dep checker on a non-Windows system"
		sys.exit(1)
	print "Checking for Dependencies"
	python_path = windows_registry.find_python()
	if opts.build:
		vs_path = windows_registry.find_visualstudio2008()
		sdk_path = windows_registry.find_MSPlatformSDK() 
	try:
		import pysvn
		print "---Found PySVN"
	except ImportError:
		print "---PySVN Not Found, Please Install"
		sys.exit(1)

	if opts.build:
		try:
			if os.path.exists(vs_path):
				print "---Found Visual Studio 9"
				if sdk_path == "":
					sdk_path = vs_path+"VC\\PlatformSDK\\"
	
				path = vs_path+"Common7\\IDE;"+vs_path+"VC\\BIN;"
				path += vs_path+"Common7\\Tools;"+frameworkdir+"v3.5;"
				path += frameworkdir+"v2.0.50727;"+vs_path+"VC\\VCPackages;"
				path += sdk_path+"bin;"
				include = vs_path+"VC\\INCLUDE;"+sdk_path+"include;"
				lib = vs_path+"VC\\LIB;"+sdk_path+"lib;"
				libpath = frameworkdir+"v3.5;"+frameworkdir+"v2.0.50727;"
				libpath += vs_path+"VC\\LIB;"
				old_path = os.environ['path']
				os.environ['path'] = path+old_path
				os.environ['include'] = include
				os.environ['lib'] = lib
				os.environ['libpath'] = libpath
		except TypeError:
			print "---Visual Studio 9 Not Found"
			sys.exit(1)

def which(program):
	def is_exe(fpath):
		return os.path.exists(fpath) and os.access(fpath, os.X_OK)
	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return exe_file
	return None

def linux(opts):
	print "Checking for Dependencies"
	try:
		import pysvn
		print "---Found PySVN"
	except ImportError:
		print "---PySVN Not Found, Please Install"
		sys.exit(1)

if __name__ == '__main__':
	win32()
