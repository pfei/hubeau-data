from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class StationHydrobio(BaseModel):
    code_station_hydrobio: Optional[str] = None
    libelle_station_hydrobio: Optional[str] = None
    uri_station_hydrobio: Optional[str] = None
    date_premier_prelevement: Optional[str] = None
    date_dernier_prelevement: Optional[str] = None
    coordonnee_x: Optional[float] = None
    coordonnee_y: Optional[float] = None
    code_projection: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    code_commune: Optional[str] = None
    libelle_commune: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None
    code_region: Optional[str] = None
    libelle_region: Optional[str] = None
    code_cours_eau: Optional[str] = None
    libelle_cours_eau: Optional[str] = None
    uri_cours_eau: Optional[str] = None
    code_masse_eau: Optional[str] = None
    libelle_masse_eau: Optional[str] = None
    uri_masse_eau: Optional[str] = None
    code_sous_bassin: Optional[str] = None
    libelle_sous_bassin: Optional[str] = None
    code_bassin: Optional[str] = None
    libelle_bassin: Optional[str] = None
    codes_reseaux: Optional[List[str]] = None
    libelles_reseaux: Optional[List[str]] = None
    codes_supports: Optional[List[str]] = None
    libelles_supports: Optional[List[str]] = None
    codes_appel_taxons: Optional[List[str]] = None
    libelles_appel_taxons: Optional[List[str]] = None
    codes_indices: Optional[List[str]] = None
    libelles_indices: Optional[List[str]] = None


class IndiceHydrobio(BaseModel):
    code_indice: Optional[str] = None
    libelle_indice: Optional[str] = None
    code_station_hydrobio: Optional[str] = None
    libelle_station_hydrobio: Optional[str] = None
    uri_station_hydrobio: Optional[str] = None
    date_prelevement: Optional[str] = None
    resultat_indice: Optional[float] = None
    unite_indice: Optional[str] = None
    coordonnee_x: Optional[float] = None
    coordonnee_y: Optional[float] = None
    code_projection: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    code_commune: Optional[str] = None
    libelle_commune: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None
    code_region: Optional[str] = None
    libelle_region: Optional[str] = None
    code_cours_eau: Optional[str] = None
    libelle_cours_eau: Optional[str] = None
    uri_cours_eau: Optional[str] = None
    code_masse_eau: Optional[str] = None
    libelle_masse_eau: Optional[str] = None
    uri_masse_eau: Optional[str] = None
    code_sous_bassin: Optional[str] = None
    libelle_sous_bassin: Optional[str] = None
    code_bassin: Optional[str] = None
    libelle_bassin: Optional[str] = None
    code_support: Optional[str] = None
    libelle_support: Optional[str] = None
    code_qualification: Optional[str] = None
    libelle_qualification: Optional[str] = None
    code_methode: Optional[str] = None
    libelle_methode: Optional[str] = None
    libelle_accreditation: Optional[str] = None
    code_prelevement: Optional[str] = None
    code_banque_reference: Optional[str] = None
    code_operation_prelevement: Optional[str] = None


class TaxonHydrobio(BaseModel):
    code_station_hydrobio: Optional[str] = None
    libelle_station_hydrobio: Optional[str] = None
    uri_station_hydrobio: Optional[str] = None
    date_prelevement: Optional[str] = None
    code_support: Optional[str] = None
    libelle_support: Optional[str] = None
    code_appel_taxon: Optional[str] = None
    libelle_appel_taxon: Optional[str] = None
    codes_taxons_parents: Optional[List[str]] = None
    libelles_taxons_parents: Optional[List[str]] = None
    code_type_resultat: Optional[str] = None
    libelle_type_resultat: Optional[str] = None
    resultat_taxon: Optional[float] = None
    code_qualification: Optional[str] = None
    libelle_qualification: Optional[str] = None
    code_methode: Optional[str] = None
    libelle_methode: Optional[str] = None
    libelle_liste_faune_flore: Optional[str] = None
    code_lot: Optional[str] = None
    hauteur_moyenne_lame_eau: Optional[float] = None
    largeur_moyenne_lame_eau: Optional[float] = None
    longueur_prospectee: Optional[float] = None
    codes_indices_operation: Optional[List[str]] = None
    coordonnee_x: Optional[float] = None
    coordonnee_y: Optional[float] = None
    code_projection: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    code_commune: Optional[str] = None
    libelle_commune: Optional[str] = None
    code_departement: Optional[str] = None
    libelle_departement: Optional[str] = None
    code_region: Optional[str] = None
    libelle_region: Optional[str] = None
    code_cours_eau: Optional[str] = None
    libelle_cours_eau: Optional[str] = None
    uri_cours_eau: Optional[str] = None
    code_masse_eau: Optional[str] = None
    libelle_masse_eau: Optional[str] = None
    uri_masse_eau: Optional[str] = None
    code_sous_bassin: Optional[str] = None
    libelle_sous_bassin: Optional[str] = None
    code_bassin: Optional[str] = None
    libelle_bassin: Optional[str] = None
    code_prelevement: Optional[str] = None
    code_banque_reference: Optional[str] = None
    code_operation_prelevement: Optional[str] = None


class StationHydrobioParams(BaseModel):
    """Query parameters for hydrobiological stations."""

    code_station_hydrobio: Optional[List[str]] = Field(
        None, description="Station code(s)"
    )
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_commune: Optional[List[str]] = Field(None, description="Commune code(s)")
    code_region: Optional[List[str]] = Field(None, description="Region code(s)")
    code_bassin: Optional[List[str]] = Field(None, description="Basin code(s)")
    code_cours_eau: Optional[List[str]] = Field(None, description="Watercourse code(s)")
    code_masse_eau: Optional[List[str]] = Field(None, description="Water body code(s)")
    codes_indices: Optional[List[str]] = Field(None, description="Index code(s)")
    codes_supports: Optional[List[str]] = Field(None, description="Support code(s)")
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("asc", pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[int] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class IndiceHydrobioParams(BaseModel):
    """Query parameters for hydrobiological indices."""

    code_station_hydrobio: Optional[List[str]] = Field(
        None, description="Station code(s)"
    )
    code_indice: Optional[List[str]] = Field(
        None, description="Index code(s): 1000=IBGN, 2928=IBMR, 5856=IBD, 7036=IPR"
    )
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_commune: Optional[List[str]] = Field(None, description="Commune code(s)")
    code_region: Optional[List[str]] = Field(None, description="Region code(s)")
    code_bassin: Optional[List[str]] = Field(None, description="Basin code(s)")
    code_cours_eau: Optional[List[str]] = Field(None, description="Watercourse code(s)")
    code_support: Optional[List[str]] = Field(None, description="Support code(s)")
    code_qualification: Optional[List[str]] = Field(
        None, description="Qualification code(s)"
    )
    date_debut_prelevement: Optional[str] = Field(
        None, description="Start date (YYYY-MM-DD)"
    )
    date_fin_prelevement: Optional[str] = Field(
        None, description="End date (YYYY-MM-DD)"
    )
    resultat_indice_min: Optional[float] = Field(None, description="Min index value")
    resultat_indice_max: Optional[float] = Field(None, description="Max index value")
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("desc", pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[int] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class TaxonHydrobioParams(BaseModel):
    """Query parameters for hydrobiological taxon lists."""

    code_station_hydrobio: Optional[List[str]] = Field(
        None, description="Station code(s)"
    )
    code_appel_taxon: Optional[List[str]] = Field(None, description="Taxon code(s)")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_commune: Optional[List[str]] = Field(None, description="Commune code(s)")
    code_region: Optional[List[str]] = Field(None, description="Region code(s)")
    code_bassin: Optional[List[str]] = Field(None, description="Basin code(s)")
    code_cours_eau: Optional[List[str]] = Field(None, description="Watercourse code(s)")
    code_support: Optional[List[str]] = Field(None, description="Support code(s)")
    code_qualification: Optional[List[str]] = Field(
        None, description="Qualification code(s)"
    )
    code_type_resultat: Optional[List[str]] = Field(
        None, description="Result type code(s)"
    )
    date_debut_prelevement: Optional[str] = Field(
        None, description="Start date (YYYY-MM-DD)"
    )
    date_fin_prelevement: Optional[str] = Field(
        None, description="End date (YYYY-MM-DD)"
    )
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("desc", pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[int] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")
