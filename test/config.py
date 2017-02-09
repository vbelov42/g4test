################################################################################
#
# config.py
#
################################################################################

import sys
import os

class internal_config:
    """
    This class is designed to handle all options required to successfully
    build and run g4test. It primarily includes path to GEANT4 and compiler
    options.
    """

    def __init__(self):
        # compiler
        self.CPP      = os.getenv("CPP") or 'cpp'
        self.CPPFLAGS = os.getenv("CPPFLAGS")
        self.CXX      = os.getenv("CXX")
        self.CXXFLAGS = os.getenv("CXXFLAGS")
        #self.LD       = os.getenv("LD")
        self.LDFLAGS  = os.getenv("LDFLAGS")
        self.LOADLIBS = os.getenv("LOADLIBS")
        self.LDLIBS   = os.getenv("LDLIBS")
        # GEANT
        #self.G4BASE   = FindGeant()
        self.G4VERSION= 0
        # ROOT
        # VGM

    def __str__(self):
        s = '{\n'
        for (k,v) in self.__dict__.items():
            if v != None: s += "  %s = '%s'\n" % (k,v)
        s += '}'
        return s

    def export(self):
        export_names = ['CPP','CPPFLAGS','CXX','CXXFLAGS','LDFLAGS','LDLIBS']
        return len([os.putenv(k,self.__dict__[k]) for k in export_names if self.__dict__[k]])

    def add(self,name,value):
        # this will raise 'KeyError' if 'name' doesn't exist
        if self.__dict__[name] != None:
            self.__dict__[name] += ' '+value
        else:
            self.__dict__[name] = value

    def UseGeant(self,hint=None):
        self.G4BASE = FindG4Directory(hint)
        if self.G4BASE:
            self.G4VERSION = FindG4Version(self.G4BASE)
        return self.G4BASE and self.G4VERSION > 0


################################################################################
import subprocess

def FindG4Directory(hint=None):
    """
    Try to find a directory where GEANT4 is installed. We don't do deep checks here.
    'hint' or G4BASE is what is excplicitely provided by user, so take it.
    Otherwise try more complicated techniques implemented in Makefile. Since this 
    process is tricky we want it to be in only one place, thus we simply call make.
    """
    # do we have any hints?
    g4dir = hint or os.environ.get('G4BASE')
    # we didn't check it, just return
    if g4dir:
        if not os.path.isdir(g4dir):
            print >>sys.stderr, "G4BASE provided (", g4dir ,") isn't a directory"
            return None
        return g4dir

    # have nothing, let's try something more powerful
    # we call make because we don't want to have two portions of search code
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
            print >>sys.stderr, cmd, "\n  returned error: ", run.returncode

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

################################################################################
def get_config(*pargs):
    """
    Central point to get config.
    """

    print "Parsing", os.path.basename(globals()['__file__'])
    cfg = internal_config()

    cfg.UseGeant(pargs[0])

    fn = 'config_local.py'
    try:
        fh = open(fn,'r')
        print "Parsing", fn
        fs = fh.read()
        fc = compile(fs,fn,'exec')
        exec(fc)
    except IOError:
        e = sys.exc_info()[1]
        if e.errno == 2: # No such file or directory
            pass
        else:
            print >>sys.stderr, "Can't open '%s': %s" % (fn, e)

    print "Configuring done"
    return cfg

################################################################################
def create_local():
    fn = 'config_local.py'
    try:
        fh = open(fn,'w')
        print >>fh,"""#

(system, host, _, _, arch) = os.uname()
#host_fqdn = socket.getfqdn()
print "    HOST=%s SYSTEM=%s ARCH=%s" % (host,system,arch)
"""
        fh.close()
    except:
        raise
    return

if __name__ == '__main__':

    cfg = get_config(sys.argv)
    print(cfg)
