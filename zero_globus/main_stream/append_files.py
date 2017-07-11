import glob
import os
import re
import sys
import subprocess

##============================================================================##
##-------------------------------                -----------------------------##
##============================================================================##
'''
Purpose:              Append files created from split_stream

Author:               Yuliana Zamora
Email:
Date Created:         June 25, 2017
Date Last Modified:   June 25, 2017
'''

##============================================================================##
##-------------------------------  ParentPath  -------------------------------##
##============================================================================##
class ParentPath:

    def __init__(self, path):
        self.path   = path
        self.id_ptr = 1

    def streamfile(self):
        outname = self.path
        with open(outname, "ab") as outfile:
            while os.path.exists(self.path+'.'+str(self.id_ptr)):
                f = self.path+'.'+str(self.id_ptr)
                with open(f,"rb") as infile:
                    outfile.write(infile.read())
                subprocess.call(["rm",f])
                self.id_ptr += 1

##============================================================================##
##---------------------------- get_parent_path() -----------------------------##
##============================================================================##
def get_parent_path(fullpath):

    pathhead, filename =  os.path.split(fullpath)
    fsplit = re.split('\.',str(filename))
    filename_root = fsplit[0]
    parentpath = pathhead + '/' + filename_root
    if (len(fsplit) < 2):
        if filename_root == 'DONE':
            parentpath = 'DONE'
        else:
            parentpath = None
    if os.path.isdir(parentpath):
        parentpath = None
    return parentpath

################################################################################
##============================================================================##
##------------------------------------ MAIN ----------------------------------##
##============================================================================##
################################################################################

## Just keep looping to check for new files:
#while True:

pathlist = glob.glob('/home/parallels/stream_transfer/zero_globus/test_files/*')

# Create dictionary of known parent files you are "streaming":
pathdict = {}
for fullpath in pathlist:

    # Call get_parent_path() to get the 'parent' path
    #     ex: fullpath = /home/file.0 -> path = /home/file
    path = get_parent_path(fullpath)

    # Ignore files that do not have a .* at the end:
    if path == None: continue

    # Exit code if a file called 'DONE' exists
    # (This is a way to stop the code nicely)
    if path == 'DONE': sys.exit(0)

    # Add a 'ParentPath' object to the dictionary for this
    # specific 'parent' path:
    if not (path in pathdict): pathdict[path] = ParentPath(path)

# Loop through the known parent paths,
# and try to write the info into a single file:
for parent in pathdict:
    pathdict[parent].streamfile()

## Sleep between loops.. Why not.
#time.sleep(1)
