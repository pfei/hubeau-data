from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class Site(BaseModel):
    altitude_site: Optional[float] = None
    code_commune_site: List[str]  # or List[Any] if unsure
    code_cours_eau: str
    code_departement: List[str]
    code_entite_hydro_site: str
    code_projection: int
    code_region: List[str]
    code_site: str
    code_systeme_alti_site: Optional[int] = None
    code_troncon_hydro_site: str
    code_zone_hydro_site: str
    commentaire_influence_generale_site: None = None
    commentaire_site: Optional[str] = None
    coordonnee_x_site: float
    coordonnee_y_site: float
    date_maj_site: str
    date_premiere_donnee_dispo_site: None = None
    geometry: Dict[str, Any]  # or use a GeoJSON model if you want
    grandeur_hydro: str
    influence_generale_site: Optional[int] = None
    latitude_site: float
    libelle_commune: List[str]
    libelle_cours_eau: Optional[str] = None
    libelle_departement: List[str]
    libelle_region: List[str]
    libelle_site: str
    longitude_site: float
    premier_mois_annee_hydro_site: int
    premier_mois_etiage_site: int
    statut_site: int
    surface_bv: Optional[float] = None
    type_contexte_loi_stat_site: Optional[List[int]] = None
    type_loi_site: Optional[List[int]] = None
    type_site: str
    uri_cours_eau: str


class Station(BaseModel):
    altitude_ref_alti_station: Optional[float] = None
    code_commune_station: str
    code_cours_eau: str
    code_departement: str
    code_finalite_station: Optional[str] = None
    code_projection: int
    code_regime_station: int
    code_region: str
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
    date_maj_station: str
    date_ouverture_station: str
    descriptif_station: Optional[str] = None
    en_service: bool
    geometry: Optional[Dict[str, Any]] = None  # or use a GeoJSON model if you want
    influence_locale_station: Optional[int] = None
    latitude_station: float
    libelle_commune: str
    libelle_cours_eau: Optional[str] = None
    libelle_departement: str
    libelle_region: str
    libelle_site: str
    libelle_station: str
    longitude_station: float
    qualification_donnees_station: int
    type_contexte_loi_stat_station: Optional[Union[int, str]] = None
    type_loi_station: Optional[Union[int, str]] = None
    type_station: str
    uri_cours_eau: str


class ObservationTr(BaseModel):
    code_continuite: Optional[int] = None  # Adjust if sometimes string
    code_methode_obs: Optional[int] = None  # API returns int
    code_qualification_obs: Optional[int] = None  # API returns int
    code_site: Optional[str] = None
    code_station: Optional[str] = None
    code_statut: Optional[int] = None  # API returns int; adjust if sometimes string
    code_systeme_alti_serie: Optional[int] = None  # API returns int
    date_debut_serie: Optional[str] = None  # or datetime, depending on your use case
    date_fin_serie: Optional[str] = None
    date_obs: Optional[str] = None
    grandeur_hydro: Optional[str] = None
    latitude: Optional[float] = None
    libelle_continuite: Optional[str] = None
    libelle_methode_obs: Optional[str] = None
    libelle_qualification_obs: Optional[str] = None
    libelle_statut: Optional[str] = None
    longitude: Optional[float] = None
    resultat_obs: Optional[float] = None  # or int, depending on data


class ObsElab(BaseModel):
    code_methode: Optional[int] = None
    code_qualification: Optional[int] = None
    code_site: Optional[str] = None
    code_station: Optional[str] = None
    code_statut: Optional[int] = None  # or str, see API
    date_obs_elab: Optional[str] = None  # or datetime
    date_prod: Optional[str] = None  # or datetime
    grandeur_hydro_elab: Optional[str] = None  # e.g. "QmnJ", "H"
    latitude: Optional[float] = None
    libelle_methode: Optional[str] = None
    libelle_qualification: Optional[str] = None
    libelle_statut: Optional[str] = None
    longitude: Optional[float] = None
    resultat_obs_elab: Optional[float] = None  # or int, depending on the data
