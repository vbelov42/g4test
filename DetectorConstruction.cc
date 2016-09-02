#include <globals.hh>
#include <G4Material.hh>
#include <G4Box.hh>
#include <G4Tubs.hh>
#include <G4Sphere.hh>
#include <G4LogicalVolume.hh>
#include <G4VisAttributes.hh>
#include <G4PVPlacement.hh>
#include <G4ThreeVector.hh>
#include <G4Navigator.hh>

#include "DetectorConstruction.hh"

using namespace CLHEP;

DetectorConstruction::DetectorConstruction()
{
  fNavigator = new G4Navigator();
}

DetectorConstruction::~DetectorConstruction()
{
  delete fNavigator;
}

void DetectorConstruction::ConstructMaterials()
{
  fVacuum_mat   = new G4Material("Vacuum"  ,  1., 1.01*g/mole, universe_mean_density, kStateGas, 3.e-18*pascal, 2.73*kelvin);
}

  const G4double detector_size = 1.5*m;
  const G4bool Invisible = true;

void DetectorConstruction::ConstructVolumes()
{
  G4VisAttributes* VisInv = new G4VisAttributes(Invisible); //Invisible mode

  const G4double world_size = detector_size*1.1;
  G4Box* World_sol = new G4Box("World_sol", world_size, world_size, world_size);
  G4LogicalVolume* World_log = new G4LogicalVolume(World_sol, fVacuum_mat, "World_log");
  World_log->SetVisAttributes(VisInv); 
  fWorld = new G4PVPlacement(0, G4ThreeVector(0.,0.,0.), World_log, "World", 0, false, 0);

  G4Sphere* Detector_sol = new G4Sphere("Detector_sol", 0., detector_size, 0., 360.*deg, 0., 180.*deg);
  G4LogicalVolume* Detector_log = new G4LogicalVolume(Detector_sol, fVacuum_mat, "Detector_log");
  fDetector = new G4PVPlacement(0, G4ThreeVector(0.,0.,0.), Detector_log, "Detector", World_log, false, 0);

}

G4VPhysicalVolume* DetectorConstruction::Construct()
{

  G4cout << "Constructing materials ... ";
  ConstructMaterials();
  G4cout << "done." << G4endl;
  G4cout << "Materials " << *G4Material::GetMaterialTable() << G4endl;

  G4cout << "detector_size = " << detector_size/CLHEP::m << " m" << G4endl;
  G4cout << "Constructing geometry ... ";
  ConstructVolumes();
  G4cout << "done." << G4endl;

  fNavigator->SetWorldVolume(fWorld);
  return fWorld;
}
