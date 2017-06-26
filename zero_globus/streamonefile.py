def one_file():
    # Input:
    filename = "filename_test"
    source_path      = "/Users/yzamora/streaming/zero_globus/test_files/"
    #dest_path        = "/Users/yzamora/streaming/zero_globus/destination/"
    nfiles           = 1
    nlines           = 10000 #

    for ifile in xrange(nfiles):
            fname_src = source_path+filename+"."+str(ifile)
            #fname_dst = dest_path+filename+"."+str(ifile)
            with open(fname_src,"wa") as f:
                iline = 0
                while True:
                    f.write("Adding line "+str(iline)+" in "+filename+"."+str(ifile)+"\n")
                    iline += 1
                    if (nlines <> 0) and (iline == nlines): break
    #subprocess.call(["mv",fname_src,fname_dst])
    print "All files Done."
one_file()
