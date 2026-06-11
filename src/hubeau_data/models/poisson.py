from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class StationPoisson(BaseModel):
    code_station: Optional[str] = None
    libelle_station: Optional[str] = None
    uri_station: Optional[str] = None
    statut_station: Optional[bool] = None
    date_modification_station: Optional[str] = None
    coordonnee_x_station: Optional[float] = None
    coordonnee_y_station: Optional[float] = None
    code_epsg_projection_station: Optional[int] = None
    code_projection_station: Optional[str] = None
    libelle_projection_station: Optional[str] = None
    localisation_precise_station: Optional[str] = None
    pk_aval: Optional[float] = None
    code_point_prelevement_aspe: Optional[str] = None
    code_point_prelevement: Optional[str] = None
    code_point_prelevement_wama: Optional[str] = None
    libelle_point_prelevement_wama: Optional[str] = None
    statut_point_prelevement: Optional[bool] = None
    date_modification_point_prelevement_aspe: Optional[str] = None
    code_support: Optional[str] = None
    libelle_support: Optional[str] = None
    uri_support: Optional[str] = None
    codes_dispositifs_collecte: Optional[List[str]] = None
    libelles_dispositifs_collecte: Optional[List[str]] = None
    mnemoniques_dispositifs_collecte: Optional[List[str]] = None
    uris_dispositifs_collecte: Optional[List[str]] = None
    objectifs_operation: Optional[List[str]] = None
    coordonnee_x_point_prelevement: Optional[float] = None
    coordonnee_y_point_prelevement: Optional[float] = None
    code_epsg_projection_point_prelevement: Optional[int] = None
    code_projection_point_prelevement: Optional[str] = None
    libelle_projection_point_prelevement: Optional[str] = None
    code_entite_hydrographique: Optional[str] = None
    libelle_entite_hydrographique: Optional[str] = None
    uri_entite_hydrographique: Optional[str] = None
    code_unite_hydrographique: Optional[str] = None
    libelle_unite_hydrographique: Optional[str] = None
    code_masse_eau: Optional[str] = None
    uri_masse_eau: Optional[str] = None
    code_commune: Optional[str] = None
    libelle_commune: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None
    code_region: Optional[str] = None
    libelle_region: Optional[str] = None
    lieu_dit_point_prelevement: Optional[str] = None
    localisation_precise_point_prelevement: Optional[str] = None
    distance_mer: Optional[float] = None
    distance_maree: Optional[float] = None
    code_bassin: Optional[str] = None
    libelle_bassin: Optional[str] = None
    formation_geologique: Optional[str] = None
    code_occupation_sol: Optional[str] = None
    libelle_occupation_sol: Optional[str] = None
    zone_huet: Optional[str] = None
    code_regime_hydrologique: Optional[str] = None
    libelle_regime_hydrologique: Optional[str] = None
    accessibilite: Optional[str] = None
    largeur_lit_mineur: Optional[float] = None
    distance_source: Optional[float] = None
    altitude: Optional[float] = None
    pente: Optional[float] = None
    surface_bassin_versant_amont: Optional[float] = None
    temperature_janvier: Optional[float] = None
    temperature_juillet: Optional[float] = None
    eligibilite_ipr_iprplus: Optional[bool] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None


class IndicateurPoisson(BaseModel):
    code_operation: Optional[str] = None
    date_operation: Optional[str] = None
    etat_avancement_operation: Optional[str] = None
    code_qualification_operation: Optional[str] = None
    libelle_qualification_operation: Optional[str] = None
    code_station: Optional[str] = None
    libelle_station: Optional[str] = None
    uri_station: Optional[str] = None
    code_point_prelevement: Optional[str] = None
    code_point_prelevement_aspe: Optional[str] = None
    code_point_prelevement_wama: Optional[str] = None
    libelle_point_prelevement_wama: Optional[str] = None
    code_commune: Optional[str] = None
    libelle_commune: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None
    code_region: Optional[str] = None
    libelle_region: Optional[str] = None
    code_bassin: Optional[str] = None
    libelle_bassin: Optional[str] = None
    code_entite_hydrographique: Optional[str] = None
    libelle_entite_hydrographique: Optional[str] = None
    protocole_peche: Optional[str] = None
    objectifs_operation: Optional[List[str]] = None
    codes_dispositifs_collecte: Optional[List[str]] = None
    libelles_dispositifs_collecte: Optional[List[str]] = None
    ipr_note: Optional[float] = None
    ipr_code_classe: Optional[str] = None
    ipr_libelle_classe: Optional[str] = None
    iprplus_note: Optional[float] = None
    iprplus_code_classe: Optional[str] = None
    iprplus_libelle_classe: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None


class ObservationPoisson(BaseModel):
    code_operation: Optional[str] = None
    date_operation: Optional[str] = None
    code_station: Optional[str] = None
    libelle_station: Optional[str] = None
    code_point_prelevement: Optional[str] = None
    code_point_prelevement_aspe: Optional[str] = None
    code_point_prelevement_wama: Optional[str] = None
    libelle_point_prelevement_wama: Optional[str] = None
    code_commune: Optional[str] = None
    libelle_commune: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None
    code_region: Optional[str] = None
    libelle_region: Optional[str] = None
    code_bassin: Optional[str] = None
    libelle_bassin: Optional[str] = None
    code_entite_hydrographique: Optional[str] = None
    libelle_entite_hydrographique: Optional[str] = None
    protocole_peche: Optional[str] = None
    objectifs_operation: Optional[List[str]] = None
    code_lot: Optional[int] = None
    code_type_lot: Optional[str] = None
    libelle_type_lot: Optional[str] = None
    effectif_lot: Optional[int] = None
    code_taxon: Optional[str] = None
    code_alternatif_taxon: Optional[str] = None
    nom_commun_taxon: Optional[str] = None
    nom_latin_taxon: Optional[str] = None
    uri_taxon: Optional[str] = None
    taille_min_lot: Optional[float] = None
    taille_max_lot: Optional[float] = None
    poids_lot_mesure: Optional[float] = None
    poids_lot_estime: Optional[float] = None
    code_individu: Optional[int] = None
    taille_individu: Optional[float] = None
    poids_individu_mesure: Optional[float] = None
    poids_individu_estime: Optional[float] = None
    sexe_individu: Optional[str] = None
    age_individu: Optional[int] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None


class OperationPoisson(BaseModel):
    code_operation: Optional[int] = None
    date_operation: Optional[str] = None
    etat_avancement_operation: Optional[str] = None
    code_qualification_operation: Optional[str] = None
    libelle_qualification_operation: Optional[str] = None
    code_station: Optional[str] = None
    libelle_station: Optional[str] = None
    uri_station: Optional[str] = None
    code_point_prelevement: Optional[str] = None
    code_point_prelevement_aspe: Optional[str] = None
    code_point_prelevement_wama: Optional[str] = None
    libelle_point_prelevement_wama: Optional[str] = None
    code_commune: Optional[str] = None
    libelle_commune: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None
    code_region: Optional[str] = None
    libelle_region: Optional[str] = None
    code_bassin: Optional[str] = None
    libelle_bassin: Optional[str] = None
    code_entite_hydrographique: Optional[str] = None
    libelle_entite_hydrographique: Optional[str] = None
    protocole_peche: Optional[str] = None
    objectifs_operation: Optional[List[str]] = None
    codes_dispositifs_collecte: Optional[List[str]] = None
    libelles_dispositifs_collecte: Optional[List[str]] = None
    temperature_instantanee: Optional[float] = None
    conductivite: Optional[float] = None
    longueur: Optional[float] = None
    largeur_lame_eau: Optional[float] = None
    profondeur: Optional[float] = None
    surface_calculee: Optional[float] = None
    operation_sans_poisson: Optional[bool] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None


class StationPoissonParams(BaseModel):
    """Query parameters for fish monitoring stations."""

    code_station: Optional[List[str]] = Field(None, description="Station code(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_commune: Optional[List[str]] = Field(None, description="Commune code(s)")
    code_region: Optional[List[str]] = Field(None, description="Region code(s)")
    code_bassin: Optional[List[str]] = Field(None, description="Basin code(s)")
    code_entite_hydrographique: Optional[List[str]] = Field(
        None, description="Hydrographic entity code(s)"
    )
    code_masse_eau: Optional[List[str]] = Field(None, description="Water body code(s)")
    altitude_min: Optional[int] = Field(None, description="Min altitude (m)")
    altitude_max: Optional[int] = Field(None, description="Max altitude (m)")
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("asc", pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class IndicateurPoissonParams(BaseModel):
    """Query parameters for fish indicators (IPR, IPR+)."""

    code_station: Optional[List[str]] = Field(None, description="Station code(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_region: Optional[List[str]] = Field(None, description="Region code(s)")
    code_bassin: Optional[List[str]] = Field(None, description="Basin code(s)")
    code_operation: Optional[List[str]] = Field(None, description="Operation code(s)")
    date_operation_min: Optional[str] = Field(
        None, description="Min operation date (YYYY-MM-DD)"
    )
    date_operation_max: Optional[str] = Field(
        None, description="Max operation date (YYYY-MM-DD)"
    )
    ipr_note_min: Optional[float] = Field(None, description="Min IPR score")
    ipr_note_max: Optional[float] = Field(None, description="Max IPR score")
    ipr_code_classe: Optional[List[str]] = Field(
        None, description="IPR class code(s): 1-5"
    )
    iprplus_note_min: Optional[float] = Field(None, description="Min IPR+ score")
    iprplus_note_max: Optional[float] = Field(None, description="Max IPR+ score")
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("desc", pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class ObservationPoissonParams(BaseModel):
    """Query parameters for fish observations."""

    code_station: Optional[List[str]] = Field(None, description="Station code(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_region: Optional[List[str]] = Field(None, description="Region code(s)")
    code_bassin: Optional[List[str]] = Field(None, description="Basin code(s)")
    code_operation: Optional[List[str]] = Field(None, description="Operation code(s)")
    code_taxon: Optional[List[str]] = Field(None, description="Taxon code(s)")
    nom_latin_taxon: Optional[List[str]] = Field(
        None, description="Latin taxon name(s)"
    )
    nom_commun_taxon: Optional[List[str]] = Field(
        None, description="Common taxon name(s)"
    )
    date_operation_min: Optional[str] = Field(None, description="Min operation date")
    date_operation_max: Optional[str] = Field(None, description="Max operation date")
    taille_individu_min: Optional[int] = Field(
        None, description="Min individual size (mm)"
    )
    taille_individu_max: Optional[int] = Field(
        None, description="Max individual size (mm)"
    )
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("desc", pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class OperationPoissonParams(BaseModel):
    """Query parameters for fish sampling operations."""

    code_station: Optional[List[str]] = Field(None, description="Station code(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_region: Optional[List[str]] = Field(None, description="Region code(s)")
    code_bassin: Optional[List[str]] = Field(None, description="Basin code(s)")
    code_operation: Optional[List[str]] = Field(None, description="Operation code(s)")
    date_operation_min: Optional[str] = Field(None, description="Min operation date")
    date_operation_max: Optional[str] = Field(None, description="Max operation date")
    protocole_peche: Optional[List[str]] = Field(
        None, description="Fishing protocol(s)"
    )
    operation_sans_poisson: Optional[bool] = Field(
        None, description="Operations without fish"
    )
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("desc", pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")
