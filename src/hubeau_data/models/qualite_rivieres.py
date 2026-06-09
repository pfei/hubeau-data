from typing import Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, ConfigDict, Field

from hubeau_data.models.geojson import Geometry

T = TypeVar("T")


# --- Envelope ---
class HubeauEnvelope(BaseModel, Generic[T]):
    count: int
    first: Optional[str] = None
    last: Optional[str] = None
    prev: Optional[str] = None
    next: Optional[str] = None
    api_version: Optional[str] = None
    data: List[T]


# --- Main Data Models ---


class AnalysePc(BaseModel):
    code_station: Optional[str] = None
    libelle_station: Optional[str] = None
    uri_station: Optional[str] = None
    code_support: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    libelle_support: Optional[str] = None
    uri_support: Optional[str] = None
    code_fraction: Optional[str] = None
    libelle_fraction: Optional[str] = None
    uri_fraction: Optional[str] = None
    date_prelevement: Optional[str] = None
    heure_prelevement: Optional[str] = None
    date_maj_analyse: Optional[str] = None
    heure_analyse: Optional[str] = None
    code_parametre: Optional[str] = None
    libelle_parametre: Optional[str] = None
    uri_parametre: Optional[str] = None
    code_groupe_parametre: Optional[List[str]] = None
    libelle_groupe_parametre: Optional[List[str]] = None
    uri_groupe_parametre: Optional[List[str]] = None
    resultat: Optional[Union[str, float, int]] = None
    code_unite: Optional[str] = None
    symbole_unite: Optional[str] = None
    uri_unite: Optional[str] = None
    code_remarque: Optional[str] = None
    mnemo_remarque: Optional[str] = None
    code_insitu: Optional[str] = None
    libelle_insitu: Optional[str] = None
    code_difficulte_analyse: Optional[str] = None
    mnemo_difficulte_analyse: Optional[str] = None
    limite_detection: Optional[float] = None
    limite_quantification: Optional[float] = None
    limite_saturation: Optional[float] = None
    incertitude_analytique: Optional[float] = None
    code_methode_fractionnement: Optional[str] = None
    nom_methode_fractionnement: Optional[str] = None
    uri_methode_fractionnement: Optional[str] = None
    code_methode_analyse: Optional[str] = None
    nom_methode_analyse: Optional[str] = None
    uri_methode_analyse: Optional[str] = None
    rendement_extraction: Optional[float] = None
    code_methode_extraction: Optional[str] = None
    nom_methode_extraction: Optional[str] = None
    uri_methode_extraction: Optional[str] = None
    code_accreditation: Optional[str] = None
    mnemo_accreditation: Optional[str] = None
    agrement: Optional[str] = None
    code_statut: Optional[str] = None
    mnemo_statut: Optional[str] = None
    code_qualification: Optional[str] = None
    libelle_qualification: Optional[str] = None
    commentaires_analyse: Optional[str] = None
    commentaires_resultat_analyse: Optional[str] = None
    code_reseau: Optional[List[str]] = None
    nom_reseau: Optional[List[str]] = None
    uri_reseau: Optional[List[str]] = None
    code_producteur_analyse: Optional[str] = None
    nom_producteur_analyse: Optional[str] = None
    uri_producteur_prelevement: Optional[str] = None
    code_preleveur: Optional[str] = None
    nom_preleveur: Optional[str] = None
    uri_preleveur: Optional[str] = None
    code_laboratoire: Optional[str] = None
    nom_laboratoire: Optional[str] = None
    uri_laboratoire: Optional[str] = None
    code_operation: Optional[str] = None
    code_prelevement: Optional[str] = None
    code_point_eau_surface: Optional[str] = None
    code_analyse: Optional[str] = None
    code_banque_reference: Optional[str] = None
    geometry: Optional[Geometry] = None  # Use GeoJSON type, forward ref if needed


class ConditionEnvironnementalePc(BaseModel):
    code_station: Optional[str] = None
    libelle_station: Optional[str] = None
    uri_station: Optional[str] = None
    code_operation_cep: Optional[str] = None
    date_prelevement: Optional[str] = None
    code_parametre: Optional[str] = None
    libelle_parametre: Optional[str] = None
    uri_parametre: Optional[str] = None
    libelle_resultat: Optional[str] = None
    resultat: Optional[str] = None
    code_unite: Optional[str] = None
    symbole_unite: Optional[str] = None
    uri_unite: Optional[str] = None
    code_remarque: Optional[str] = None
    mnemo_remarque: Optional[str] = None
    code_groupe_parametre: Optional[List[str]] = None
    code_statut: Optional[str] = None
    libelle_groupe_parametre: Optional[List[str]] = None
    mnemo_statut: Optional[str] = None
    code_qualification: Optional[str] = None
    uri_groupe_parametre: Optional[List[str]] = None
    code_masse_deau: Optional[str] = None
    libelle_qualification: Optional[str] = None
    code_eu_masse_deau: Optional[str] = None
    commentaire: Optional[str] = None
    date_mesure: Optional[str] = None
    nom_masse_deau: Optional[str] = None
    heure_mesure: Optional[str] = None
    longitude: Optional[float] = None
    code_methode: Optional[str] = None
    latitude: Optional[float] = None
    nom_methode: Optional[str] = None
    uri_methode: Optional[str] = None
    code_producteur: Optional[str] = None
    nom_producteur: Optional[str] = None
    uri_producteur: Optional[str] = None
    code_preleveur: Optional[str] = None
    nom_preleveur: Optional[str] = None
    uri_preleveur: Optional[str] = None
    code_banque_reference: Optional[str] = None
    code_point_eau_surface: Optional[str] = None
    code_prelevement: Optional[str] = None
    date_maj: Optional[str] = None
    geometry: Optional[Geometry] = None  # Use GeoJSON type, forward ref if needed


class OperationPc(BaseModel):
    code_station: Optional[str] = None
    libelle_station: Optional[str] = None
    uri_station: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    x_prelevement: Optional[float] = None
    y_prelevement: Optional[float] = None
    code_projection: Optional[str] = None
    libelle_projection: Optional[str] = None
    code_support: Optional[str] = None
    libelle_support: Optional[str] = None
    uri_support: Optional[str] = None
    code_methode: Optional[str] = None
    nom_methode: Optional[str] = None
    uri_methode: Optional[str] = None
    date_prelevement: Optional[str] = None
    date_fin: Optional[str] = None
    heure_fin: Optional[str] = None
    heure_prelevement: Optional[str] = None
    code_zone_verticale_prospectee: Optional[str] = None
    mnemo_zone_verticale_prospectee: Optional[str] = None
    profondeur: Optional[float] = None
    code_difficulte: Optional[str] = None
    mnemo_difficulte: Optional[str] = None
    code_accreditation: Optional[str] = None
    mnemo_accreditation: Optional[str] = None
    agrement: Optional[str] = None
    code_finalite: Optional[str] = None
    libelle_finalite: Optional[str] = None
    commentaires: Optional[str] = None
    code_reseau: Optional[List[str]] = None
    nom_reseau: Optional[List[str]] = None
    uri_reseau: Optional[List[str]] = None
    code_producteur: Optional[str] = None
    nom_producteur: Optional[str] = None
    uri_producteur: Optional[str] = None
    code_preleveur: Optional[str] = None
    nom_preleveur: Optional[str] = None
    uri_preleveur: Optional[str] = None
    code_operation: Optional[str] = None
    code_prelevement: Optional[str] = None
    code_point_eau_surface: Optional[str] = None
    code_banque_reference: Optional[str] = None
    geometry: Optional[Geometry] = None  # Use GeoJSON type, forward ref if needed


class StationPc(BaseModel):
    code_station: Optional[str] = None
    libelle_station: Optional[str] = None
    uri_station: Optional[str] = None
    durete: Optional[float] = None
    coordonnee_x: Optional[float] = None
    coordonnee_y: Optional[float] = None
    code_projection: Optional[str] = None
    libelle_projection: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    code_commune: Optional[str] = None
    libelle_commune: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None
    code_region: Optional[str] = None
    libelle_region: Optional[str] = None
    code_cours_eau: Optional[str] = None
    nom_cours_eau: Optional[str] = None
    uri_cours_eau: Optional[str] = None
    nom_masse_deau: Optional[str] = None
    code_masse_deau: Optional[str] = None
    code_eu_masse_deau: Optional[str] = None
    uri_masse_deau: Optional[str] = None
    code_eu_sous_bassin: Optional[str] = None
    nom_sous_bassin: Optional[str] = None
    uri_sous_bassin: Optional[str] = None
    code_bassin: Optional[str] = None
    code_eu_bassin: Optional[str] = None
    nom_bassin: Optional[str] = None
    uri_bassin: Optional[str] = None
    type_entite_hydro: Optional[str] = None
    commentaire: Optional[str] = None
    date_creation: Optional[str] = None
    date_arret: Optional[str] = None
    date_maj_information: Optional[str] = None
    finalite: Optional[str] = None
    localisation_precise: Optional[str] = None
    nature: Optional[str] = None
    altitude_point_caracteristique: Optional[float] = None
    point_kilometrique: Optional[float] = None
    premier_mois_annee_etiage: Optional[Union[str, int]] = None
    superficie_bassin_versant_reel: Optional[float] = None
    superficie_bassin_versant_topo: Optional[float] = None
    geometry: Optional["Geometry"] = None  # Use GeoJSON type, forward ref if needed


# --- Query Params models ---


class StationPcParams(BaseModel):
    """
    Query parameters for physico-chemical monitoring stations.
    see: https://hubeau.eaufrance.fr/page/api-qualite-cours-deau#/
    """

    code_station: Optional[List[str]] = Field(
        None, description="Station code(s) Sandre"
    )
    libelle_station: Optional[List[str]] = Field(None, description="Station label(s)")
    code_commune: Optional[List[str]] = Field(None, description="Commune code(s) INSEE")
    libelle_commune: Optional[List[str]] = Field(None, description="Commune label(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    libelle_departement: Optional[List[str]] = Field(
        None, description="Department label(s)"
    )
    code_region: Optional[List[str]] = Field(None, description="Region code(s) INSEE")
    libelle_region: Optional[List[str]] = Field(None, description="Region label(s)")
    code_cours_eau: Optional[List[str]] = Field(None, description="Watercourse code(s)")
    nom_cours_eau: Optional[List[str]] = Field(None, description="Watercourse name(s)")
    code_masse_eau: Optional[List[str]] = Field(None, description="Water body code(s)")
    code_bassin_dce: Optional[List[str]] = Field(
        None, description="Basin code(s) Sandre"
    )
    code_sous_bassin: Optional[List[str]] = Field(None, description="Sub-basin code(s)")
    type_entite_hydro: Optional[List[str]] = Field(
        None, description="Hydrographic entity type(s)"
    )
    size: Optional[int] = Field(
        None, ge=1, le=20000, description="Page size (max 20000)"
    )
    sort: Optional[str] = Field(
        "asc", pattern="^(asc|desc)$", description="Sort order by code_station"
    )
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class AnalysePcParams(BaseModel):
    """
    Query parameters for physico-chemical analyses.
    see: https://hubeau.eaufrance.fr/page/api-qualite-cours-deau#/
    """

    code_station: Optional[List[str]] = Field(
        None, description="Station code(s) Sandre"
    )
    libelle_station: Optional[List[str]] = Field(None, description="Station label(s)")
    code_parametre: Optional[List[str]] = Field(
        None, description="Parameter code(s) Sandre"
    )
    libelle_parametre: Optional[List[str]] = Field(
        None, description="Parameter label(s)"
    )
    code_support: Optional[List[str]] = Field(None, description="Support code(s)")
    code_fraction: Optional[List[str]] = Field(
        None, description="Fraction code(s) Sandre"
    )
    code_groupe_parametres: Optional[List[str]] = Field(
        None, description="Parameter group code(s)"
    )
    code_qualification: Optional[List[str]] = Field(
        None, description="Qualification code(s)"
    )
    code_statut: Optional[List[str]] = Field(None, description="Status code(s)")
    code_reseau: Optional[List[str]] = Field(None, description="Network code(s)")
    code_commune: Optional[List[str]] = Field(None, description="Commune code(s) INSEE")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_region: Optional[List[str]] = Field(None, description="Region code(s) INSEE")
    code_cours_eau: Optional[List[str]] = Field(None, description="Watercourse code(s)")
    code_masse_eau: Optional[List[str]] = Field(None, description="Water body code(s)")
    code_bassin_dce: Optional[List[str]] = Field(None, description="Basin code(s)")
    code_sous_bassin: Optional[List[str]] = Field(None, description="Sub-basin code(s)")
    code_operation: Optional[List[str]] = Field(None, description="Operation code(s)")
    date_debut_prelevement: Optional[str] = Field(
        None, description="Sample start date (YYYY-MM-DD)"
    )
    date_fin_prelevement: Optional[str] = Field(
        None, description="Sample end date (YYYY-MM-DD)"
    )
    date_debut_maj: Optional[str] = Field(
        None, description="Update start date (YYYY-MM-DD)"
    )
    date_fin_maj: Optional[str] = Field(
        None, description="Update end date (YYYY-MM-DD)"
    )
    size: Optional[int] = Field(
        None, ge=1, le=20000, description="Page size (max 20000)"
    )
    sort: Optional[str] = Field(
        "asc", pattern="^(asc|desc)$", description="Sort order by date_prelevement"
    )
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


# --- Envelope Aliases ---
JsonAnalysePc = HubeauEnvelope[AnalysePc]
JsonConditionEnvironnementalePc = HubeauEnvelope[ConditionEnvironnementalePc]
JsonOperationPc = HubeauEnvelope[OperationPc]
JsonStationPc = HubeauEnvelope[StationPc]
