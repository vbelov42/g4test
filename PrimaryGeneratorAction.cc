#include <globals.hh>
#include <G4GeneralParticleSource.hh>
#include <G4Event.hh>

#include "PrimaryGeneratorAction.hh"

PrimaryGeneratorAction::PrimaryGeneratorAction()
 :gps(0)
{
  gps = new G4GeneralParticleSource();
}

PrimaryGeneratorAction::~PrimaryGeneratorAction()
{
  if (gps) delete gps;
}

void PrimaryGeneratorAction::GeneratePrimaries(G4Event* event)
{
  gps->GeneratePrimaryVertex(event);
}
