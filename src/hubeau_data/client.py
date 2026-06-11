from hubeau_data.api.hydrometrie import HydrometrieAPI
from hubeau_data.api.piezometrie import PiezometrieAPI
from hubeau_data.api.qualite_nappes import QualiteNappesAPI
from hubeau_data.api.qualite_rivieres import QualiteRivieresAPI


class HubeauClient:
    """Unified client for the Hubeau APIs.
    Access sub-APIs as .qualite_rivieres and .hydrometrie attributes.
    """

    def __init__(self) -> None:
        self.qualite_rivieres = QualiteRivieresAPI()
        self.hydrometrie = HydrometrieAPI()
        self.piezometrie = PiezometrieAPI()
        self.qualite_nappes = QualiteNappesAPI()
