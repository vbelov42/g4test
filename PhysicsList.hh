#ifndef PhysicsList_hh
#define PhysicsList_hh

#include <G4VUserPhysicsList.hh>

class PhysicsList: public G4VUserPhysicsList
{
  public:
    PhysicsList();
   ~PhysicsList();

  protected:
    void ConstructParticle();
    void ConstructProcess();
    void SetCuts();

};

#endif
