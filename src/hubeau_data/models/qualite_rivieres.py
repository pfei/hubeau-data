from typing import Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel

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


# --- Envelope Aliases ---
JsonAnalysePc = HubeauEnvelope[AnalysePc]
JsonConditionEnvironnementalePc = HubeauEnvelope[ConditionEnvironnementalePc]
JsonOperationPc = HubeauEnvelope[OperationPc]
JsonStationPc = HubeauEnvelope[StationPc]
