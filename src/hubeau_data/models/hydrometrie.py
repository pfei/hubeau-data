from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class Site(BaseModel):
    altitude_site: Optional[float] = None
    code_commune_site: Optional[List[str]] = None
    code_cours_eau: Optional[str] = None
    code_departement: Optional[List[str]] = None
    code_entite_hydro_site: Optional[str] = None
    code_projection: int
    code_region: Optional[List[str]] = None
    code_site: str
    code_systeme_alti_site: Optional[int] = None
    code_troncon_hydro_site: Optional[str] = None
    code_zone_hydro_site: Optional[str] = None
    commentaire_influence_generale_site: None = None
    commentaire_site: Optional[str] = None
    coordonnee_x_site: float
    coordonnee_y_site: float
    date_maj_site: Optional[str] = None
    date_premiere_donnee_dispo_site: None = None
    geometry: Dict[str, Any]
    grandeur_hydro: Optional[str] = None
    influence_generale_site: Optional[int] = None
    latitude_site: float
    libelle_commune: Optional[List[str]] = None
    libelle_cours_eau: Optional[str] = None
    libelle_departement: Optional[List[str]] = None
    libelle_region: Optional[List[str]] = None
    libelle_site: Optional[str] = None
    longitude_site: float
    premier_mois_annee_hydro_site: int
    premier_mois_etiage_site: int
    statut_site: int
    surface_bv: Optional[float] = None
    type_contexte_loi_stat_site: Optional[List[int]] = None
    type_loi_site: Optional[List[int]] = None
    type_site: Optional[str] = None
    uri_cours_eau: Optional[str] = None


class Station(BaseModel):
    altitude_ref_alti_station: Optional[float] = None
    code_commune_station: Optional[str] = None
    code_cours_eau: Optional[str] = None
    code_departement: Optional[str] = None
    code_finalite_station: Optional[str] = None
    code_projection: int
    code_regime_station: int
    code_region: Optional[str] = None
    code_sandre_reseau_station: Optional[List[Any]] = None
    code_site: str
    code_station: str
    code_systeme_alti_site: Optional[int] = None
    commentaire_influence_locale_station: Optional[str] = None
    commentaire_station: Optional[str] = None
    coordonnee_x_station: float
    coordonnee_y_station: float
    date_activation_ref_alti_station: Optional[str] = None
    date_debut_ref_alti_station: Optional[str] = None
    date_fermeture_station: Optional[str] = None
    date_maj_ref_alti_station: Optional[str] = None
    date_maj_station: Optional[str] = None
    date_ouverture_station: Optional[str] = None
    descriptif_station: Optional[str] = None
    en_service: bool
    geometry: Optional[Dict[str, Any]] = None
    influence_locale_station: Optional[int] = None
    latitude_station: float
    libelle_commune: Optional[str] = None
    libelle_cours_eau: Optional[str] = None
    libelle_departement: Optional[str] = None
    libelle_region: Optional[str] = None
    libelle_site: Optional[str] = None
    libelle_station: Optional[str] = None
    longitude_station: float
    qualification_donnees_station: int
    type_contexte_loi_stat_station: Optional[Union[int, str]] = None
    type_loi_station: Optional[Union[int, str]] = None
    type_station: Optional[str] = None
    uri_cours_eau: Optional[str] = None


class ObservationTr(BaseModel):
    code_continuite: Optional[int] = None
    code_methode_obs: Optional[int] = None
    code_qualification_obs: Optional[int] = None
    code_site: Optional[str] = None
    code_station: Optional[str] = None
    code_statut: Optional[int] = None
    code_systeme_alti_serie: Optional[int] = None
    date_debut_serie: Optional[str] = None
    date_fin_serie: Optional[str] = None
    date_obs: Optional[str] = None
    grandeur_hydro: Optional[str] = None
    latitude: Optional[float] = None
    libelle_continuite: Optional[str] = None
    libelle_methode_obs: Optional[str] = None
    libelle_qualification_obs: Optional[str] = None
    libelle_statut: Optional[str] = None
    longitude: Optional[float] = None
    resultat_obs: Optional[float] = None


class ObsElab(BaseModel):
    code_methode: Optional[int] = None
    code_qualification: Optional[int] = None
    code_site: Optional[str] = None
    code_station: Optional[str] = None
    code_statut: Optional[int] = None
    date_obs_elab: Optional[str] = None
    date_prod: Optional[str] = None
    grandeur_hydro_elab: Optional[str] = None
    latitude: Optional[float] = None
    libelle_methode: Optional[str] = None
    libelle_qualification: Optional[str] = None
    libelle_statut: Optional[str] = None
    longitude: Optional[float] = None
    resultat_obs_elab: Optional[float] = None


# --- Query Params models ---


class SiteParams(BaseModel):
    """
    Query parameters for hydrometric sites.
    see: https://hubeau.eaufrance.fr/page/api-hydrometrie#/hydrometrie/sites
    """

    code_site: Optional[List[str]] = Field(None, description="Site code(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_commune_site: Optional[List[str]] = Field(None, description="Commune code(s)")
    code_region: Optional[List[str]] = Field(None, description="Region code(s)")
    code_cours_eau: Optional[str] = Field(None, description="Watercourse code")
    libelle_site: Optional[str] = Field(None, description="Site label (partial match)")
    type_site: Optional[str] = Field(None, description="Site type")
    size: Optional[int] = Field(
        None, ge=1, le=10000, description="Maximum number of results"
    )
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class StationParams(BaseModel):
    """
    Query parameters for hydrometric stations.
    see: https://hubeau.eaufrance.fr/page/api-hydrometrie#/hydrometrie/stations
    """

    code_station: Optional[List[str]] = Field(None, description="Station code(s)")
    code_site: Optional[List[str]] = Field(None, description="Site code(s)")
    code_commune_station: Optional[str] = Field(None, description="Commune code")
    code_departement: Optional[str] = Field(None, description="Department code")
    code_region: Optional[str] = Field(None, description="Region code")
    code_cours_eau: Optional[str] = Field(None, description="Watercourse code")
    libelle_station: Optional[str] = Field(
        None, description="Station label (partial match)"
    )
    en_service: Optional[bool] = Field(None, description="In service filter")
    size: Optional[int] = Field(
        None, ge=1, le=10000, description="Maximum number of results"
    )
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class ObsElabParams(BaseModel):
    """
    Query parameters for elaborated hydrometric observations.
    see: https://hubeau.eaufrance.fr/page/api-hydrometrie#/hydrometrie/obs_elab
    """

    code_station: Optional[List[str]] = Field(None, description="Station code(s)")
    code_site: Optional[List[str]] = Field(None, description="Site code(s)")
    grandeur_hydro_elab: Optional[str] = Field(
        None, description="QmnJ, QmM, HIXM, HIXnJ, QINM, QINnJ, QixM, QIXnJ"
    )
    date_debut_obs_elab: Optional[str] = Field(
        None, description="Start date (ISO 8601)"
    )
    date_fin_obs_elab: Optional[str] = Field(None, description="End date (ISO 8601)")
    resultat_min: Optional[float] = None
    resultat_max: Optional[float] = None
    size: Optional[int] = Field(None, ge=1, le=20000)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")
    sort: Optional[str] = Field("asc", pattern="^(asc|desc)$")

    model_config = ConfigDict(extra="allow")


class ObservationTrParams(BaseModel):
    """
    Query parameters for hydrometric real-time observations.
    'Tr' is 'Temps réel'
    see: https://hubeau.eaufrance.fr/page/api-hydrometrie#/hydrometrie/observations
    """

    code_station: Optional[List[str]] = Field(None, description="Station code(s)")
    code_site: Optional[List[str]] = Field(None, description="Site code(s)")
    grandeur_hydro: Optional[List[str]] = Field(
        None, description="Hydrometric magnitude: H (height) or Q (flow)"
    )
    date_debut_obs: Optional[str] = Field(None, description="Start date (ISO 8601)")
    date_fin_obs: Optional[str] = Field(None, description="End date (ISO 8601)")
    size: Optional[int] = Field(
        None, ge=1, le=20000, description="Maximum number of results"
    )
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")
    sort: Optional[str] = Field(
        "desc", pattern="^(asc|desc)$", description="Sort order by date_obs"
    )

    model_config = ConfigDict(extra="allow")
