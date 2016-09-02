#ifndef PrimaryGeneratorAction_hh
#define PrimaryGeneratorAction_hh

#include <G4VUserPrimaryGeneratorAction.hh>

class G4GeneralParticleSource;
class G4Event;

class PrimaryGeneratorAction: public G4VUserPrimaryGeneratorAction
{
  public:
    PrimaryGeneratorAction();
    ~PrimaryGeneratorAction();

    void GeneratePrimaries(G4Event*);

  private:
    G4GeneralParticleSource *gps;

};

#endif
