import  os, subprocess, shutil

def make(make_opts):
    config_cmd = ["cmake ../",
    	"-DPREFIX="+make_opts.mangos_destdir,
	"-DPCH=1",
	"-DACE_USE_EXTERNAL=1",
	"-DTBB_USE_EXTERNAL=1",
	#"-DLIBS=\"-framework Carbon\""
	];

    if make_opts.debug: print " ".join(config_cmd)
    print "Install Dir: ", make_opts.mangos_destdir
    if make_opts.debug: print "Current Dir: ", os.getcwd()
    if os.path.basename(os.getcwd()) != "MaNGOS":
        os.chdir("MaNGOS")
    if make_opts.debug: print "Current Dir: ", os.getcwd()
    if os.path.exists("build"):
        shutil.rmtree("build", ignore_errors=True)
    os.mkdir("build")
    os.chdir("build")
    if make_opts.debug: print "Current Dir: ", os.getcwd()
    subprocess.call(" ".join(config_cmd), shell=True)
    subprocess.call("make", shell=True)
