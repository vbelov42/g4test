G4BASE ?= /opt/geant4/4.10.00.p02/sl5-64

G4CONFIG := $(wildcard $(G4BASE)/bin/geant4-config)
G4ENV = $(G4BASE)/bin/geant4.sh
G4INC := $(filter -D% -I% -W%, $(shell $(G4CONFIG) --cflags))
G4LIBS := $(shell $(G4CONFIG) --libs)

CPPFLAGS += -D_GNU_SOURCE -DG4VIS_USE
CXXFLAGS += $(G4INC) -ggdb -fPIC
LDFLAGS += -ggdb
LDLIBS += $(G4LIBS) 

.PHONY: all
all: g4test

-include depend

OBJECTS = \
    DetectorConstruction.o PrimaryGeneratorAction.o PhysicsList.o \
    g4test.o

g4test: $(OBJECTS)
	$(CXX) $(LDFLAGS) -o $@ $^ $(LDLIBS)

run: depend g4test
	source $(G4ENV); \
	  set; \
	  LD_LIBRARY_PATH+=$(G4BASE)/lib/geant4/Linux-g++:$$LD_LIBRARY_PATH ./g4test;

depend: Makefile
	echo depend: $(wildcard *.cc) >depend
	$(CXX) -M $(CXXFLAGS) $(wildcard *.cc) >>depend

clean:
	rm -f *.o *_Dict.* depend

tar:
	tar -czf g4test.tgz Makefile EXOSim *.hh *.cc *LinkDef.h *.mac
