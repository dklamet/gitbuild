#!/usr/bin/env python3

import os
import time
import subprocess
import re

branch="integration"
repo="user@server.domain:path/repo.git"

#Time format used for temporary build directory name:w

TIMEFORMAT="%H:%M:%S:%m-%d-%Y"

def getProgramOutput(cmd):
    fd=os.popen(cmd)
    lines=[]
    line=fd.readline()
    while line:
        lines.append(line)
        line=fd.readline()

    return lines
   

def getTimeStamp():
    return time.strftime(TIMEFORMAT,time.localtime())

def getCommit(line):
    match=re.search(r"commit\s+([0-9a-f]+)\s+",line)
    return match.group(1)

def getTags(line):
    return re.findall(r"tag: (\d+\.\S+)(?:,|\))",line)



datestamp=getTimeStamp()

dir=branch+datestamp

subprocess.call(["git","clone", "-n",repo,dir],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

currentdir=os.getcwd()
os.chdir(dir)

retval=subprocess.call(["git","checkout",branch],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
if retval:
    print("Initial checkout failed: {d}\n",retval)
    exit(1)

commitlist=getProgramOutput("git log -m --name-status --decorate=short |grep -e '^commit' |grep \'tag: \'")

#pat=re.compile("\((?:(?tag: (\d+\.\d+(?:,|\)))))+)")
taglist=[]
for line in commitlist:
    tags=getTags(line);
    commit=getCommit(line);

    if len(tags):
        #print(commit)
        #print(tags)
        #print()
        taglist.append(tuple((tags[0],commit)))
os.chdir(currentdir)

for (tag,commit) in taglist:

    if not os.path.exists(tag):
        os.chdir(dir)
        os.system("git checkout "+tag+">/dev/null 2>&1")
        os.system("git clean -f")
        os.system("git clean -f")
        os.system("git submodule init")
        os.system("git submodule update")
        if os.path.exists("makefile"): 
            cmdstring="bash -c \"make -f makefile >"+tag+".log 2>&1\""
        else:
            cmdstring="bash -c \"make >"+tag+".log 2>&1\""
        retval=os.system(cmdstring)
        os.chdir(currentdir)
        
        if retval:
            print("Make failed error: {0:d}\n".format(retval))
            os.rename(dir,tag+":FAILED")
        else:
            print("Made tag {0:s}".format(tag))
            os.rename(dir,tag)
        
        subprocess.call(["git","clone", "-n",repo,dir],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    else:
        print("Tag: {0!s} already built".format(tag))

#Remove temporary build directory
if os.path.exists(dir):
    os.system("rm -rf "+dir)

