from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class StationEcoulement(BaseModel):
    code_station: Optional[str] = None
    libelle_station: Optional[str] = None
    uri_station: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None
    code_commune: Optional[str] = None
    libelle_commune: Optional[str] = None
    code_region: Optional[str] = None
    libelle_region: Optional[str] = None
    code_bassin: Optional[str] = None
    libelle_bassin: Optional[str] = None
    coordonnee_x_station: Optional[float] = None
    coordonnee_y_station: Optional[float] = None
    code_projection_station: Optional[str] = None
    libelle_projection_station: Optional[str] = None
    code_epsg_station: Optional[str] = None
    code_cours_eau: Optional[str] = None
    libelle_cours_eau: Optional[str] = None
    uri_cours_eau: Optional[str] = None
    etat_station: Optional[str] = None
    date_maj_station: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ObservationEcoulement(BaseModel):
    code_station: Optional[str] = None
    libelle_station: Optional[str] = None
    uri_station: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None
    code_commune: Optional[str] = None
    libelle_commune: Optional[str] = None
    code_region: Optional[str] = None
    libelle_region: Optional[str] = None
    code_bassin: Optional[str] = None
    libelle_bassin: Optional[str] = None
    coordonnee_x_station: Optional[float] = None
    coordonnee_y_station: Optional[float] = None
    code_projection_station: Optional[str] = None
    libelle_projection_station: Optional[str] = None
    code_cours_eau: Optional[str] = None
    libelle_cours_eau: Optional[str] = None
    uri_cours_eau: Optional[str] = None
    code_campagne: Optional[str] = None
    code_reseau: Optional[str] = None
    libelle_reseau: Optional[str] = None
    uri_reseau: Optional[str] = None
    date_observation: Optional[str] = None
    code_ecoulement: Optional[str] = None
    libelle_ecoulement: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CampagneEcoulement(BaseModel):
    code_campagne: Optional[int] = None
    date_campagne: Optional[str] = None
    nombre_modalite_ecoulement: Optional[int] = None
    code_type_campagne: Optional[int] = None
    libelle_type_campagne: Optional[str] = None
    code_reseau: Optional[str] = None
    libelle_reseau: Optional[str] = None
    uri_reseau: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None


class StationEcoulementParams(BaseModel):
    """
    Query parameters for flow stations.
    see: https://hubeau.eaufrance.fr/page/api-ecoulement
    """

    code_station: Optional[List[str]] = Field(None, description="Station code(s)")
    libelle_station: Optional[List[str]] = Field(None, description="Station label(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_commune: Optional[List[str]] = Field(None, description="Commune code(s)")
    code_region: Optional[List[str]] = Field(None, description="Region code(s)")
    code_bassin: Optional[List[str]] = Field(None, description="Basin code(s)")
    code_cours_eau: Optional[List[str]] = Field(None, description="Watercourse code(s)")
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("asc", pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class ObservationEcoulementParams(BaseModel):
    """
    Query parameters for flow observations.
    see: https://hubeau.eaufrance.fr/page/api-ecoulement
    """

    code_station: Optional[List[str]] = Field(None, description="Station code(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_commune: Optional[List[str]] = Field(None, description="Commune code(s)")
    code_region: Optional[List[str]] = Field(None, description="Region code(s)")
    code_bassin: Optional[List[str]] = Field(None, description="Basin code(s)")
    code_cours_eau: Optional[List[str]] = Field(None, description="Watercourse code(s)")
    code_campagne: Optional[List[str]] = Field(None, description="Campaign code(s)")
    code_reseau: Optional[List[str]] = Field(None, description="Network code(s)")
    code_ecoulement: Optional[List[str]] = Field(
        None, description="Flow modality code(s): 1/1a/1f/2/3/4"
    )
    date_observation_min: Optional[str] = Field(
        None, description="Min date (YYYY-MM-DD)"
    )
    date_observation_max: Optional[str] = Field(
        None, description="Max date (YYYY-MM-DD)"
    )
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field(None, pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class CampagneEcoulementParams(BaseModel):
    """
    Query parameters for flow campaigns.
    see: https://hubeau.eaufrance.fr/page/api-ecoulement
    """

    code_campagne: Optional[List[int]] = Field(None, description="Campaign code(s)")
    code_type_campagne: Optional[List[int]] = Field(
        None, description="Campaign type: 1 (Usuelle) or 2 (Complémentaire)"
    )
    code_reseau: Optional[List[str]] = Field(None, description="Network code(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    date_campagne_min: Optional[str] = Field(None, description="Min date (YYYY-MM-DD)")
    date_campagne_max: Optional[str] = Field(None, description="Max date (YYYY-MM-DD)")
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field(None, pattern="^(asc|desc)$")

    model_config = ConfigDict(extra="allow")
