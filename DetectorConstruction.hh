#ifndef DetectorConstruction_hh
#define DetectorConstruction_hh

#include <G4VUserDetectorConstruction.hh>

class G4VPhysicalVolume;
class G4Material;
class G4Navigator;
class G4VTouchable;

class DetectorConstruction: public G4VUserDetectorConstruction
{
    public:
	DetectorConstruction();
	~DetectorConstruction();

	G4VPhysicalVolume* Construct();
	inline G4VPhysicalVolume* GetWorldVolume() const { return fWorld; }

        G4Navigator* GetNavigator() { return fNavigator; }

    private:

	void ConstructMaterials();
	void ConstructVolumes();

	G4Material* fVacuum_mat;
	G4VPhysicalVolume* fWorld;
	G4VPhysicalVolume* fDetector;
	G4Navigator *fNavigator;
};	

#endif /* DetectorConstruction_hh */
