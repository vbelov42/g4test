#!/usr/bin/python2
# Let's be compatible with RHEL5, that means 2.4

import sys
import os
import subprocess
from optparse import OptionParser;


def FindG4Directory(hint=None):
    """
    Try to find a directory where GEANT4 is installed. We don't do deep checks here.
    'hint' or G4BASE is what is excplicitely provided by user, so take it.
    Otherwise try more complicated techniques implemented in Makefile. Since this 
    process is tricky we want it to be in only one place, thus we simply call make.
    """
    # do we have any hints?
    g4dir = hint or os.environ.get('G4BASE')

    if not g4dir:
        # now lets try something more powerful
        cmd = "G4BASE='' make -C .. -s g4base 2>&1"
        try:
            run = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
        except OSError:
    	    e = sys.exc_info()[1]
            print >>sys.stderr, "Execution of 'make g4base' failed:", e
        else:
            run.wait()
            if run.returncode==0:
                g4dir = run.stdout.readline().strip()
            else:
                print >>sys.stderr, "'make g4base' returned error: ", run.returncode

    # we tried everything, either we have it or not
    return g4dir

def FindG4Version(g4dir=None):
    """
    Determine version for a GEANT4 installation provided.
    Here we simply take it from headder file directly without compilation to
    simplify our life.
    """
    g4ver = None
    ls = [ 
        "include/Geant4/G4Version.hh", # G4.10
        "include/geant4/G4Version.hh", # G4.9.3 all_include
        "source/global/management/include/G4Version.hh", # G4.9.3 no_all_include
    ]
    for name in ls:
        print "trying file",name
        try:
            fh = open(os.path.join(g4dir,name))
        except IOError:
    	    e = sys.exc_info()[1]
            print e
        else:
            for line in fh:
                words = line.strip().split(' ')
                if (words[0]=='#define' and words[1]=='G4VERSION_NUMBER'):
                    g4ver = " ".join(words[2:]).strip()
            fh.close()
        if g4ver: break
    return int(g4ver)

def BuildTest(options):
    print "make test"
    cmd = "make G4BASE=%s -C .. clean g4test >%s 2>&1" % (options.g4dir, os.path.join(options.result_path,'make.log'))
    ret = os.system(cmd)
    if not ret == 0:
        print >>sys.stderr, "Build fail, see make.log for details"
    return ret==0

def RunTest(options):
    print "run test"
    cmd = "make G4BASE=%s -C .. run >%s 2>%s" % (options.g4dir, os.path.join(options.result_path,'test.out'), os.path.join(options.result_path,'test.err'))
    ret = os.system(cmd)
    if not ret == 0:
        print >>sys.stderr, "Run fail, see test.err for details"

    # should we copy any *.root files produced ?

    # should we check test.err ?
    return ret==0

if __name__ == '__main__':
    usage = "%prog [options] <test> <result> [G4DIR]"
    parser = OptionParser(usage)
    #parser.add_option("-t",dest="test",default="-0",help="set ID of test to use")
    #parser.add_option("-r",dest="result",default="",help="set ID for result")
    parser.add_option("-f",dest="force",action='store_true',default=False,help="force <result> overwrite")
    parser.add_option("-g",dest="g4dir",default="",help="set GEANT4 installation path")
    (options, args) = parser.parse_args()

    options.result = 'custom'
    if len(args) > 0:
        options.test = args[0]
    if len(args) > 1:
        options.result = args[1]
    if len(args) > 2:
        options.g4dir = args[2]
    if len(args) == 0 or len(args) > 3:
        parser.print_help()
        sys.exit(1)
    sys.argv = args
    print "args=",args

    # find GEANT4
    if not options.g4dir:
        options.g4dir = FindG4Directory()
    print "g4dir=",options.g4dir
    if not options.g4dir:
	print >>sys.stderr, "Can't find GEANT4 installation"
	sys.exit(2)
    options.g4version = FindG4Version(options.g4dir)
    print "g4ver=",options.g4version
    if options.g4version < 900:
        print >>sys.stderr, "Your GEANT4 setup is too old and unsupported:", options.g4version
        sys.exit(2)

    # find test
    if not os.path.isdir(options.test):
        print >>sys.stderr, "Can't find test '"+options.test+"'"
        sys.exit(3)
    if   os.path.isfile(os.path.join(options.test,'test.py')):
        print "Test type Not implemented"
    elif os.path.isfile(os.path.join(options.test,'test.mac')):
        print "Test type 'simple'"
    else:
        print >>sys.stderr, "Can't find test in:", options.test
        sys.exit(3)

    # check result
    options.result_path = os.path.join(options.test,options.result)
    try:
        files = os.listdir(options.result_path)
        # it is a directory
        if len(files):
            # and it contains something
            print >>sys.stderr, "Result directory isn't empty"
            if not options.force:
                sys.exit(3)
    except OSError:
    	e = sys.exc_info()[1]
        if e.errno == 2: # No such file or directory
            # let's create it
            try:
                os.mkdir(options.result_path,0755)
            except OSError:
                e = sys.exc_info()[1]
                print >>sys.stderr, "Can't create result directory:", e
                sys.exit(3)
        else:
            print >>sys.stderr, "Can't create result directory:", e
            sys.exit(3)

    # now with g4ver and test we could tune some build parameters
    # TBD

    # ready for rock'n'roll
    print(options)
    if not BuildTest(options):
        sys.exit(4)
    if not RunTest(options):
        sys.exit(5)
    print "Done"
