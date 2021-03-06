#

# Either will be empty if not found
ifneq ($(G4BASE),)
  # If G4BASE is set, use GEANT from there
  G4CONFIG := $(wildcard $(G4BASE)/bin/geant4-config)
  G4ENV := $(wildcard $(G4BASE)/src/geant4/.config/bin/*/env.sh)
else
  # Otherwise try to find any GEANT
  G4CONFIG := $(shell which geant4-config 2>/dev/null)
  G4ENV := $(wildcard $(G4INSTALL)/.config/bin/*/env.sh)
endif

ifneq ($(G4CONFIG),)
  # This is available since 9.5 with cmake build system
  # Take everything from config provided
  G4BASE := $(shell cd `$(G4CONFIG) --prefix`; pwd)
  G4ENV := $(subst /geant4-config,/geant4.sh,$(G4CONFIG))
  G4INC := $(filter -D% -I% -W%, $(shell $(G4CONFIG) --cflags-without-gui))
  G4LIBS := $(shell $(G4CONFIG) --libs-without-gui)
else ifneq ($(G4ENV),)
  # This is an old shell-based build system
  # Guess from config environment provided
  G4BASE := $(G4INSTALL)
  G4INC := $(shell source $(G4ENV) >/dev/null; if [ -n "$$G4INCLUDE" ]; then echo -n " -I$$G4INCLUDE"; else find $$G4INSTALL -name include -printf " -I%p"; fi; echo -n " -I$$CLHEP_INCLUDE_DIR")
  G4LIBS := $(shell source $(G4ENV) >/dev/null; echo -L$$G4LIB/$$G4SYSTEM; cd $$G4LIB/$$G4SYSTEM; ls -1 libG4*.so | sed 's/^lib/-l/; s/\.so//;'; echo -L$$CLHEP_LIB_DIR -l$$CLHEP_LIB)
else ifneq ($(G4SYSTEM),)
  # Looks like shell variables are set, use it
  G4BASE = $(G4INSTALL)
  G4INC := $(shell if [ -n "$$G4INCLUDE" ]; then echo -n " -I$$G4INCLUDE"; else find $$G4INSTALL -name include -printf " -I%p"; fi; echo -n " -I$$CLHEP_INCLUDE_DIR")
  G4LIBS := $(shell echo -L$$G4LIB/$$G4SYSTEM; cd $$G4LIB/$$G4SYSTEM; ls -1 libG4*.so | sed 's/^lib/-l/; s/\.so//;'; echo -L$$CLHEP_LIB_DIR -l$$CLHEP_LIB)
else
  # We have nothing and don't know what to do
  $(error Can't find GEANT4. Please set G4BASE to a directory where GEANT4 is installed.) #'
endif

CPPFLAGS += -D_GNU_SOURCE -DG4VIS_USE
CXXFLAGS += $(G4INC) -ggdb -fPIC
LDFLAGS += -ggdb
LDLIBS += $(G4LIBS)

SYSTEM := (shell uname -s)
ifeq ($(SYSTEM),Linux)
  RP_OPTION ?= -Wl,-rpath,
  RUN_PATH = -rdynamic $(subst -L,$(RP_OPTION),$(filter -L%, $(LDFLAGS) $(LDLIBS)))
endif

.PHONY: all g4base
all: g4test

ifeq ($(filter $(MAKECMDGOALS),clean g4base),)
-include depend
endif

OBJECTS = \
    DetectorConstruction.o PrimaryGeneratorAction.o PhysicsList.o \
    g4test.o

g4base:
	@echo $(G4BASE)
# remember situations like /usr/lib64/alsa-lib/

g4test: $(OBJECTS)
	$(CXX) $(LDFLAGS) $(RUN_PATH) -o $@ $^ $(LDLIBS)

run: depend g4test
	source $(G4ENV); \
	  set; \
	    ./g4test;

depend: Makefile
	echo depend: $(wildcard *.cc) >depend
	$(CXX) -M $(CXXFLAGS) $(wildcard *.cc) >>depend

clean:
	rm -f *.o *_Dict.* depend

tar:
	tar -czf g4test.tgz Makefile EXOSim *.hh *.cc *LinkDef.h *.mac
