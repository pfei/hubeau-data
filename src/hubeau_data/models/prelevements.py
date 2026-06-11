from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class OuvragePrelevement(BaseModel):
    code_ouvrage: Optional[str] = None
    id_local_ouvrage: Optional[str] = None
    nom_ouvrage: Optional[str] = None
    date_exploitation_debut: Optional[str] = None
    date_exploitation_fin: Optional[str] = None
    code_precision_coord: Optional[str] = None
    libelle_precision_coord: Optional[str] = None
    commentaire: Optional[str] = None
    code_commune_insee: Optional[str] = None
    nom_commune: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None
    code_type_milieu: Optional[str] = None
    libelle_type_milieu: Optional[str] = None
    code_entite_hydro_cours_eau: Optional[str] = None
    uri_entite_hydro_cours_eau: Optional[str] = None
    code_entite_hydro_plan_eau: Optional[str] = None
    uri_entite_hydro_plan_eau: Optional[str] = None
    code_mer_ocean: Optional[str] = None
    ressource_cont_non_referencee: Optional[bool] = None
    ressource_cont_non_referencee_info: Optional[str] = None
    code_point_referent: Optional[str] = None
    code_bdlisa: Optional[str] = None
    uri_bdlisa: Optional[List[str]] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    codes_points_prelevements: Optional[List[str]] = None
    uri_ouvrage: Optional[str] = None


class PointPrelevement(BaseModel):
    code_point_prelevement: Optional[str] = None
    nom_point_prelevement: Optional[str] = None
    date_exploitation_debut: Optional[str] = None
    date_exploitation_fin: Optional[str] = None
    code_type_milieu: Optional[str] = None
    libelle_type_milieu: Optional[str] = None
    code_nature: Optional[str] = None
    libelle_nature: Optional[str] = None
    lieu_dit: Optional[str] = None
    commentaire: Optional[str] = None
    code_commune_insee: Optional[str] = None
    nom_commune: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None
    code_entite_hydro_cours_eau: Optional[str] = None
    uri_entite_hydro_cours_eau: Optional[str] = None
    code_entite_hydro_plan_eau: Optional[str] = None
    uri_entite_hydro_plan_eau: Optional[str] = None
    code_zone_hydro: Optional[str] = None
    uri_zone_hydro: Optional[str] = None
    code_mer_ocean: Optional[str] = None
    code_bdlisa: Optional[List[str]] = None
    uri_bdlisa: Optional[List[str]] = None
    nappe_accompagnement: Optional[bool] = None
    code_bss_point_eau: Optional[str] = None
    uri_bss_point_eau: Optional[str] = None
    code_ouvrage: Optional[str] = None
    uri_ouvrage: Optional[str] = None


class ChroniquePrelevement(BaseModel):
    code_ouvrage: Optional[str] = None
    nom_ouvrage: Optional[str] = None
    uri_ouvrage: Optional[str] = None
    annee: Optional[int] = None
    volume: Optional[float] = None
    code_usage: Optional[str] = None
    libelle_usage: Optional[str] = None
    code_statut_volume: Optional[str] = None
    libelle_statut_volume: Optional[str] = None
    code_qualification_volume: Optional[str] = None
    libelle_qualification_volume: Optional[str] = None
    code_statut_instruction: Optional[str] = None
    libelle_statut_instruction: Optional[str] = None
    code_mode_obtention_volume: Optional[str] = None
    libelle_mode_obtention_volume: Optional[str] = None
    prelevement_ecrasant: Optional[bool] = None
    producteur_donnee: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    code_commune_insee: Optional[str] = None
    nom_commune: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None


class OuvrageParams(BaseModel):
    """Query parameters for water withdrawal structures."""

    code_ouvrage: Optional[List[str]] = Field(None, description="Structure code(s)")
    nom_ouvrage: Optional[List[str]] = Field(None, description="Structure name(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_commune_insee: Optional[List[str]] = Field(None, description="Commune code(s)")
    code_type_milieu: Optional[List[str]] = Field(
        None, description="Medium type: CONT, LIT, SOUT"
    )
    code_bdlisa: Optional[List[str]] = Field(None, description="BDLISA code(s)")
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("asc", pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class PointPrelevementParams(BaseModel):
    """Query parameters for water withdrawal points."""

    code_point_prelevement: Optional[List[str]] = Field(
        None, description="Point code(s)"
    )
    code_ouvrage: Optional[List[str]] = Field(None, description="Structure code(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_commune_insee: Optional[List[str]] = Field(None, description="Commune code(s)")
    code_type_milieu: Optional[List[str]] = Field(
        None, description="Medium type: CONT, LIT, SOUT"
    )
    code_nature: Optional[List[str]] = Field(
        None, description="Nature: F (fictif), P (physique)"
    )
    code_bss_point_eau: Optional[List[str]] = Field(None, description="BSS code(s)")
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("asc", pattern="^(asc|desc)$")

    model_config = ConfigDict(extra="allow")


class ChroniquePrelevementParams(BaseModel):
    """Query parameters for annual water withdrawal volumes."""

    code_ouvrage: Optional[List[str]] = Field(None, description="Structure code(s)")
    annee: Optional[List[int]] = Field(None, description="Year(s) of withdrawal")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_commune_insee: Optional[List[str]] = Field(None, description="Commune code(s)")
    code_usage: Optional[List[str]] = Field(None, description="Usage code(s)")
    code_type_milieu: Optional[List[str]] = Field(None, description="Medium type(s)")
    code_qualification_volume: Optional[List[str]] = Field(
        None, description="Volume qualification code(s)"
    )
    code_statut_volume: Optional[List[str]] = Field(
        None, description="Volume status code(s)"
    )
    code_statut_instruction: Optional[List[str]] = Field(
        None, description="Instruction status: AUT, DEM, REA"
    )
    code_mode_obtention_volume: Optional[List[str]] = Field(
        None, description="Volume obtention mode(s)"
    )
    volume_min: Optional[float] = Field(None, description="Min volume (m3)")
    volume_max: Optional[float] = Field(None, description="Max volume (m3)")
    prelevement_ecrasant: Optional[bool] = Field(
        None, description="High-volume low-retention withdrawal"
    )
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("asc", pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")
