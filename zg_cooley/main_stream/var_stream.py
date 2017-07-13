##============================================================================##
##------------------------------- stream_queue.py ----------------------------##
##============================================================================##
'''
Purpose:              Various types of streaming. Multiple files, bytes into one
                       file, and a controller.

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         July 10, 2017
Date Last Modified:   July 10, 2017
'''

##============================================================================##
##-------------------------------- mult_files() ------------------------------##
##============================================================================##


#Creating multiple files. If file_number set to 0, create infinite files
def mult_files(file_number):
	filename = "filename_test"
	source_path      = "/home/parallels/stream_transfer/zero_globus/test_files/"
	#dest_path        = "/tmp/ramdisk/"
	max_iterations   = file_number

	#if   len(sys.argv) == 1: filename = filename_default
	#elif len(sys.argv) == 2: filename = sys.argv[1]
	#else:
	#    print "Syntax: python stream_onefile.py <FILE-optional>"
	#    sys.exit(1)

	iter = 0
	while True:
	    random_num = int(random.random()*1000000000)
	    #fname_src = source_path+filename+"."+str(random_num)
	    #fname_dst = dest_path+filename+"."+str(random_num)
	    fname_src = source_path+filename+"."+str(iter)
	    #fname_dst = dest_path+filename+"."+str(iter)
	    with open(fname_src,"wa") as f: f.write(str(iter)+"\n")
	    #subprocess.call(["mv",fname_src,fname_dst])
	    iter += 1
            if (file_number != 0):
	        if iter == max_iterations:
	            print "Max Iteration Reached. Done."; break

##============================================================================##
##-------------------------------- one_file() --------------------------------##
##============================================================================##
#Creating one file with multiple lines. If nlines =0, infinite lines
def one_file():
	# Input:
    filename = "filename_test"
    source_path      = "/home/parallels/stream_transfer/zero_globus/test_files2/"
    #dest_path        = "/Users/yzamora/streaming/zero_globus/destination/"
    nfiles           = 1
    nlines           = 0 #if zero infinite lines

    for ifile in xrange(nfiles):
            fname_src = source_path+filename+"."+str(ifile)
            #fname_dst = dest_path+filename+"."+str(ifile)
            with open(fname_src,"wr+") as f:
                iline = 0
                while True:
                    f.write("Adding line "+str(iline)+" in "+filename+"."+str(ifile)+"\n")
                    iline += 1
                    if (nlines <> 0) and (iline == nlines): break
    #subprocess.call(["mv",fname_src,fname_dst])
    print "All files Done."

##============================================================================##
##-------------------------------- stream_child() ----------------------------##
##============================================================================##
#Calls mult_file in a child thread
def stream_child():
    #file_number = input("How many files would you like to create? Enter 0 for infinite: ")
    if (file_number == 0): print ("Creating a streaming set of files. Ctrl+Z or C to stop")
    try:
        pid = os.fork()
        if pid == 0:
            #Chilff thread calls function
            mult_files(file_number)
            os._exit(0)
        else:
            if file_number ==0: time.sleep(1)
            #will exit so parent thread can work
            else: os.waitpid(pid,0)
            return
    except OSError, e:
        print >>sys.stderr, "fork failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)
