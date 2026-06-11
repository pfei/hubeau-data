from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class StationTemperature(BaseModel):
    code_station: Optional[str] = None
    libelle_station: Optional[str] = None
    uri_station: Optional[str] = None
    localisation: Optional[str] = None
    coordonnee_x: Optional[float] = None
    coordonnee_y: Optional[float] = None
    code_type_projection: Optional[int] = None
    libelle_type_projection: Optional[str] = None
    premier_mois_etiage: Optional[int] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    code_commune: Optional[str] = None
    libelle_commune: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None
    code_region: Optional[str] = None
    libelle_region: Optional[str] = None
    code_troncon_hydro: Optional[str] = None
    code_cours_eau: Optional[str] = None
    libelle_cours_eau: Optional[str] = None
    uri_cours_eau: Optional[str] = None
    code_masse_eau: Optional[str] = None
    libelle_masse_eau: Optional[str] = None
    uri_masse_eau: Optional[str] = None
    code_sous_bassin: Optional[str] = None
    libelle_sous_bassin: Optional[str] = None
    code_bassin: Optional[str] = None
    code_eu_bassin: Optional[str] = None
    code_eu_masse_eau: Optional[str] = None
    libelle_bassin: Optional[str] = None
    nature_station: Optional[str] = None
    type_entite_hydro: Optional[str] = None
    uri_sous_bassin: Optional[str] = None
    uri_bassin: Optional[str] = None
    commentaire: Optional[str] = None
    pk: Optional[float] = None
    altitude: Optional[float] = None
    superficie_reelle: Optional[float] = None
    superficie_topo: Optional[float] = None
    date_maj_infos: Optional[str] = None
    date_mise_en_service: Optional[str] = None
    date_mise_hors_service: Optional[str] = None
    geometry: Optional[Dict[str, Any]] = None


class ChroniqueTemperature(BaseModel):
    code_station: Optional[str] = None
    libelle_station: Optional[str] = None
    localisation: Optional[str] = None
    uri_station: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    code_commune: Optional[str] = None
    libelle_commune: Optional[str] = None
    code_cours_eau: Optional[str] = None
    libelle_cours_eau: Optional[str] = None
    uri_cours_eau: Optional[str] = None
    code_parametre: Optional[str] = None
    libelle_parametre: Optional[str] = None
    date_mesure_temp: Optional[str] = None
    heure_mesure_temp: Optional[str] = None
    resultat: Optional[float] = None
    code_unite: Optional[str] = None
    symbole_unite: Optional[str] = None
    code_qualification: Optional[str] = None
    libelle_qualification: Optional[str] = None


class StationTemperatureParams(BaseModel):
    """
    Query parameters for temperature monitoring stations.
    see: https://hubeau.eaufrance.fr/page/api-temperature-continu
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
    code_masse_eau: Optional[List[str]] = Field(None, description="Water body code(s)")
    date_debut_mesure: Optional[str] = Field(
        None, description="Start date (YYYY-MM-DD)"
    )
    date_fin_mesure: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("asc", pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class ChroniqueTemperatureParams(BaseModel):
    """
    Query parameters for temperature time series.
    see: https://hubeau.eaufrance.fr/page/api-temperature-continu
    """

    code_station: Optional[List[str]] = Field(None, description="Station code(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_commune: Optional[List[str]] = Field(None, description="Commune code(s)")
    code_region: Optional[List[str]] = Field(None, description="Region code(s)")
    code_bassin: Optional[List[str]] = Field(None, description="Basin code(s)")
    code_cours_eau: Optional[List[str]] = Field(None, description="Watercourse code(s)")
    code_masse_eau: Optional[List[str]] = Field(None, description="Water body code(s)")
    code_qualification: Optional[List[str]] = Field(
        None, description="Qualification code(s)"
    )
    code_statut: Optional[List[str]] = Field(None, description="Status code(s)")
    date_debut_mesure: Optional[str] = Field(
        None, description="Start date (YYYY-MM-DD)"
    )
    date_fin_mesure: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    resultat_min: Optional[float] = Field(None, description="Min temperature value")
    resultat_max: Optional[float] = Field(None, description="Max temperature value")
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("asc", pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")
