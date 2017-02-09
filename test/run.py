#!/usr/bin/env python2
# Let's be compatible with RHEL5, that means 2.4

import sys
import os
import subprocess
from optparse import OptionParser
from config import get_config


def BuildTest(cfg):
    print "make test"
    cfg.export()
    cmd = "make G4BASE=%s -C .. clean g4test >%s 2>&1" % (cfg.G4BASE, os.path.join(cfg.result_dir,'make.log'))
    ret = os.system(cmd)
    if not ret == 0:
        print >>sys.stderr, "Build fail, see make.log for details"
    return ret==0

def RunTest(cfg):
    print "run test"
    cmd = "make G4BASE=%s -C .. run >%s 2>%s" % (cfg.G4BASE, os.path.join(cfg.result_dir,'test.out'), os.path.join(cfg.result_dir,'test.err'))
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
    print options
    cfg = get_config(options.g4dir)
    if not cfg.G4BASE:
        print >>sys.stderr, "Can't find GEANT4 installation"
        sys.exit(2)
    print "g4dir=", cfg.G4BASE
    print "g4ver=", cfg.G4VERSION
    if cfg.G4VERSION < 900:
        print >>sys.stderr, "Your GEANT4 setup is too old and unsupported:", cfg.G4VERSION
        sys.exit(2)

    # find test
    if not os.path.isdir(options.test):
        print >>sys.stderr, "Can't find test '"+options.test+"'"
        sys.exit(3)
    if   os.path.isfile(os.path.join(options.test,'test.py')):
        print "Test type Not implemented"
        cfg.test_type = 'python'
    elif os.path.isfile(os.path.join(options.test,'test.mac')):
        print "Test type 'simple'"
        cfg.test_type = 'simple'
    else:
        print >>sys.stderr, "Can't find test in:", options.test
        sys.exit(3)
    cfg.test = options.test

    # check result
    cfg.result = options.result
    cfg.result_dir = os.path.join(options.test,options.result)
    try:
        files = os.listdir(cfg.result_dir)
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
                os.mkdir(cfg.result_dir,0755)
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
    print cfg
    if not BuildTest(cfg):
        sys.exit(4)
    if not RunTest(cfg):
        sys.exit(5)
    print "Done"
