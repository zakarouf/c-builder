#!/usr/bin/env python3
import os, sys, fnmatch
from subprocess import Popen
from datetime import datetime


folderIgnore={""}
IgnoreNames={}

ignorePatternFront = ["."]
ignorePatternEnd = []
onlyTakePatternEnd = [".c"]

CC="clang"
CFLAGS=["-std=c99", "-ffunction-sections", "-fdata-sections", "-Os", "-O2"]
LDFLAGS=""
OUTEXE="cb-out"

testCommands = []

# Global End

def run(commands):
    Popen(commands).wait()


def log(msg):
    print(msg, end='')


def checkIfNameFound(name, nArray):
    for i in nArray:
        if fnmatch.fnmatch(name, "*"+i):
            return 1
    return 0

def compile(cfiles):

    cf = cfiles.split(" ")

    run_command = [ CC ] + CFLAGS

    for i in cf:
        run_command.append(i)
    run_command.append('-o')
    run_command.append(OUTEXE)
    
    run([ "rm","-rf","build" ])
    run(["mkdir", "build"])
    run(run_command)


def getallFiles(dirName):
    log("Getting C files...")
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        dirnames[:] = [d for d in dirnames if d not in folderIgnore]
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]


    log("DONE\n\n")

    return listOfFiles


def filterListintoFile(ls):

    log("Filtering Files...")
    outstr = "" 
    for elem in ls:
        if elem[2] != ".":
            if elem[-1] == "c":
                if checkIfNameFound(elem, IgnoreNames) != 1:
                    outstr += elem + " "
                    log("\n\t\tGot: " + elem)

    log("\nCOMPLETED\n\n")
    return outstr

def do_clean():
        log("Cleaning...")
        run(["rm", "-rf", "build"])
        log("DONE\n")

def main(source, clean, testCommands):
    if clean:
        do_clean()
        return

    # Get the list of all files in directory tree at given path
    outstr = filterListintoFile(getallFiles(source))

    log("Compiling...")



    compile(outstr)
    log("DONE\n\n")

    log("Executable: " + OUTEXE + "\n\n")

    log("Testing...\n")
    try:
        run([ "./"+OUTEXE] + testCommands)
    except:
        log("FAILED\n")
        return
    log("\nSUCCESS\n")

def argp(arg):
    source = "./"
    cleanEnabled = 0
    testEnabled = 1
    count = 0
    for i in arg:
        if i[0] == '-':
            if i[1:] == "-clean" or i[1:] == 'c':
                cleanEnabled= 1
            elif i[1:] == "-build" or i[1:] == 'b':
                source = arg[count+1]
            elif i[1:] == "-testdisable" or i[1:] == 't':
                testEnabled = 0
            elif i[1:] == "-testwith" or i[1:] == 'w':
                testCommands = arg[count::]
            else:
                pass

    main(source, cleanEnabled, testCommands)
    


if __name__ == '__main__':

    now = datetime.now()

    timestamp = datetime.timestamp(now)

    log("Starting...\n\n")
    argp(sys.argv)
    log("\nEND\n")
    
    timest1 = datetime.timestamp(datetime.now())
    print("Time Elasped...{:.3} total".format(timest1 - timestamp) )
