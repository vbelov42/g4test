#include <G4RunManager.hh>
#include <G4UImanager.hh>
#include <Randomize.hh>

#include "DetectorConstruction.hh"
#include "PhysicsList.hh"
#include "PrimaryGeneratorAction.hh"

int main (int argc, char **argv)
{
  G4RunManager           *fRunManager;
  G4UImanager            *fUIManager;

  {
    fRunManager = new G4RunManager();
    CLHEP::HepRandom::showEngineStatus();
//    G4cout << "rand " << CLHEP::HepRandom::getTheEngine()->getSeed() << " " << CLHEP::HepRandom::getTheEngine()->flat() << " " << G4endl;
    fRunManager->SetUserInitialization(new DetectorConstruction());
    fRunManager->SetUserInitialization(new PhysicsList());
    fRunManager->SetUserAction(new PrimaryGeneratorAction());
    fRunManager->Initialize();
    fUIManager = G4UImanager::GetUIpointer();
    fUIManager->ApplyCommand("/control/verbose 1");
    fUIManager->ApplyCommand("/tracking/verbose 1");
    fUIManager->ApplyCommand("/run/initialize");
    fUIManager->ApplyCommand("/run/beamOn 1");
    if (fRunManager) delete fRunManager;
    fRunManager = 0;
  }

  return 0;
}
