from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class StationPiezo(BaseModel):
    bss_id: Optional[str] = None
    code_bss: Optional[str] = None
    urn_bss: Optional[str] = None
    altitude_station: Optional[str] = None
    code_departement: Optional[str] = None
    nom_departement: Optional[str] = None
    code_commune_insee: Optional[str] = None
    nom_commune: Optional[str] = None
    libelle_pe: Optional[str] = None
    nb_mesures_piezo: Optional[int] = None
    profondeur_investigation: Optional[float] = None
    date_debut_mesure: Optional[str] = None
    date_fin_mesure: Optional[str] = None
    date_maj: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None
    codes_masse_eau_edl: Optional[List[str]] = None
    noms_masse_eau_edl: Optional[List[str]] = None
    urns_masse_eau_edl: Optional[List[str]] = None
    codes_bdlisa: Optional[List[str]] = None
    urns_bdlisa: Optional[List[str]] = None
    geometry: Optional[Dict[str, Any]] = None


class ChroniquePiezo(BaseModel):
    bss_id: Optional[str] = None
    code_bss: Optional[str] = None
    urn_bss: Optional[str] = None
    date_mesure: Optional[str] = None
    timestamp_mesure: Optional[int] = None
    niveau_nappe_eau: Optional[float] = None
    profondeur_nappe: Optional[float] = None
    mode_obtention: Optional[str] = None
    statut: Optional[str] = None
    qualification: Optional[str] = None
    code_continuite: Optional[str] = None
    nom_continuite: Optional[str] = None
    code_nature_mesure: Optional[str] = None
    nom_nature_mesure: Optional[str] = None
    code_producteur: Optional[str] = None
    nom_producteur: Optional[str] = None


class StationPiezoParams(BaseModel):
    """
    Query parameters for piezometric stations.
    see: https://hubeau.eaufrance.fr/page/api-piezometrie
    """

    bss_id: Optional[List[str]] = Field(None, description="New BSS code(s)")
    code_bss: Optional[List[str]] = Field(None, description="Old BSS code(s)")
    code_commune: Optional[List[str]] = Field(None, description="INSEE commune code(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_bdlisa: Optional[List[str]] = Field(
        None, description="BDLISA hydrogeological entity code(s)"
    )
    codes_masse_eau_edl: Optional[List[str]] = Field(
        None, description="Water body code(s)"
    )
    nb_mesures_piezo_min: Optional[int] = Field(
        None, description="Minimum number of piezometric measurements"
    )
    date_recherche: Optional[str] = Field(
        None, description="Active stations at date (yyyy-MM-dd)"
    )
    size: Optional[int] = Field(
        None, ge=1, le=20000, description="Page size (max 20000)"
    )
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class ChroniquePiezoParams(BaseModel):
    """
    Query parameters for piezometric time series.
    see: https://hubeau.eaufrance.fr/page/api-piezometrie
    """

    bss_id: Optional[List[str]] = Field(None, description="New BSS code(s)")
    code_bss: Optional[List[str]] = Field(None, description="Old BSS code(s)")
    date_debut_mesure: Optional[str] = Field(
        None, description="Start date (yyyy-MM-dd)"
    )
    date_fin_mesure: Optional[str] = Field(None, description="End date (yyyy-MM-dd)")
    size: Optional[int] = Field(
        None, ge=1, le=20000, description="Page size (max 20000)"
    )
    sort: Optional[str] = Field(
        "asc", pattern="^(asc|desc)$", description="Sort by date_mesure"
    )

    model_config = ConfigDict(extra="allow")
