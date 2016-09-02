#include <globals.hh>
//#include "G4ios.hh"
#include <G4Version.hh>
#include <G4SystemOfUnits.hh>
#include <G4UnitsTable.hh>
#include <G4ProcessManager.hh>
#include <G4ParticleTypes.hh>

#include "PhysicsList.hh"

PhysicsList::PhysicsList(): G4VUserPhysicsList()
{
  SetVerboseLevel(1);
  defaultCutValue  = 10.0*mm;
}

PhysicsList::~PhysicsList()
{}

#include <G4BosonConstructor.hh>
#include <G4LeptonConstructor.hh>
#include <G4MesonConstructor.hh>
#include <G4BaryonConstructor.hh>
#include <G4IonConstructor.hh>
#include <G4ShortLivedConstructor.hh>

void PhysicsList::ConstructParticle()
{
  // As of version 4.10 all used particles MUST be created in here,
  // so we are firing anything just for the case
  G4Geantino::GeantinoDefinition();
  G4BosonConstructor::ConstructParticle();
  G4LeptonConstructor::ConstructParticle();
  G4MesonConstructor::ConstructParticle();
  G4BaryonConstructor::ConstructParticle();
  G4IonConstructor::ConstructParticle();
  G4ShortLivedConstructor::ConstructParticle();
}

void PhysicsList::ConstructProcess()
{
  AddTransportation();

  if (verboseLevel>2) {
    theParticleIterator->reset();
    while( (*theParticleIterator)() ){
      G4ParticleDefinition* particle = theParticleIterator->value();
      G4ProcessManager* pmanager = particle->GetProcessManager();
      pmanager->DumpInfo();
    }
  }
}

void PhysicsList::SetCuts()
{
  if (verboseLevel >0){
    G4cout << "EXOOldPhysicsList::SetCuts:";
    G4cout << "CutLength : " << G4BestUnit(defaultCutValue,"Length") << G4endl;
  }
  G4ProductionCutsTable::GetProductionCutsTable()->SetEnergyRange(50*eV, 100*MeV);
  if (verboseLevel>0) DumpCutValuesTable();
}
