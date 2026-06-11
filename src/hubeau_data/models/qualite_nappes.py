from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class StationNappe(BaseModel):
    bss_id: Optional[str] = None
    code_bss: Optional[str] = None
    urn_bss: Optional[str] = None
    date_debut_mesure: Optional[str] = None
    date_fin_mesure: Optional[str] = None
    precision_coordonnees: Optional[int] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    altitude: Optional[str] = None
    code_insee: Optional[str] = None
    nom_commune: Optional[str] = None
    num_departement: Optional[str] = None
    nom_departement: Optional[str] = None
    nom_region: Optional[str] = None
    bassin_dce: Optional[str] = None
    code_bassin_dce: Optional[str] = None
    urn_bassin_dce: Optional[str] = None
    circonscriptions_administrative_bassin: Optional[List[str]] = None
    libelle_pe: Optional[str] = None
    code_nature_pe: Optional[int] = None
    nom_nature_pe: Optional[str] = None
    uri_nature_pe: Optional[str] = None
    code_caracteristique_aquifere: Optional[str] = None
    nom_caracteristique_aquifere: Optional[str] = None
    uri_caracteristique_aquifere: Optional[str] = None
    code_etat_pe: Optional[int] = None
    nom_etat_pe: Optional[str] = None
    uri_etat_pe: Optional[str] = None
    code_mode_gisement: Optional[int] = None
    nom_mode_gisement: Optional[str] = None
    uri_mode_gisement: Optional[str] = None
    profondeur_investigation: Optional[float] = None
    commentaire_pe: Optional[str] = None
    codes_entite_hg_bdlisa: Optional[List[str]] = None
    noms_entite_hg_bdlisa: Optional[List[str]] = None
    urns_bdlisa: Optional[List[str]] = None
    codes_masse_eau_rap: Optional[List[str]] = None
    noms_masse_eau_rap: Optional[List[str]] = None
    urns_masse_eau_rap: Optional[List[str]] = None
    codes_masse_eau_edl: Optional[List[str]] = None
    noms_masse_eau_edl: Optional[List[str]] = None
    urns_masse_eau_edl: Optional[List[str]] = None
    codes_reseau: Optional[List[str]] = None
    noms_reseau: Optional[List[str]] = None
    uris_reseau: Optional[List[str]] = None
    geometry: Optional[Dict[str, Any]] = None


class AnalyseNappe(BaseModel):
    bss_id: Optional[str] = None
    code_bss: Optional[str] = None
    urn_bss: Optional[str] = None
    precision_coordonnees: Optional[int] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    altitude: Optional[str] = None
    code_insee_actuel: Optional[str] = None
    nom_commune_actuel: Optional[str] = None
    num_departement: Optional[str] = None
    nom_departement: Optional[str] = None
    code_region: Optional[str] = None
    nom_region: Optional[str] = None
    code_circonscription_administrative_bassin: Optional[str] = None
    nom_circonscription_administrative_bassin: Optional[str] = None
    code_bassin_dce: Optional[str] = None
    nom_bassin_dce: Optional[str] = None
    urn_bassin_dce: Optional[str] = None
    code_type_point_eau: Optional[int] = None
    nom_type_point_eau: Optional[str] = None
    code_type_qualito: Optional[int] = None
    nom_type_qualito: Optional[str] = None
    uri_type_qualito: Optional[str] = None
    code_producteur: Optional[str] = None
    nom_producteur: Optional[str] = None
    uri_producteur: Optional[str] = None
    date_debut_prelevement: Optional[str] = None
    code_param: Optional[int] = None
    nom_param: Optional[str] = None
    uri_param: Optional[str] = None
    code_fraction: Optional[int] = None
    nom_fraction: Optional[str] = None
    uri_fraction: Optional[str] = None
    resultat: Optional[float] = None
    code_remarque_analyse: Optional[int] = None
    nom_remarque_analyse: Optional[str] = None
    uri_remarque_analyse: Optional[str] = None
    code_lieu_analyse: Optional[int] = None
    nom_lieu_analyse: Optional[str] = None
    uri_lieu_analyse: Optional[str] = None
    code_methode: Optional[int] = None
    nom_methode: Optional[str] = None
    uri_methode: Optional[str] = None
    code_unite: Optional[str] = None
    nom_unite: Optional[str] = None
    uri_unite: Optional[str] = None
    symbole_unite: Optional[str] = None
    code_statut_analyse: Optional[str] = None
    nom_statut_analyse: Optional[str] = None
    uri_statut_analyse: Optional[str] = None
    code_qualification: Optional[str] = None
    nom_qualification: Optional[str] = None
    uri_qualification: Optional[str] = None
    limite_quantification: Optional[float] = None
    limite_detection: Optional[float] = None
    seuil_saturation: Optional[float] = None
    incertitude_analytique: Optional[float] = None
    codes_entite_hg_bdlisa: Optional[List[str]] = None
    noms_entite_hg_bdlisa: Optional[List[str]] = None
    urns_bdlisa: Optional[List[str]] = None
    codes_masse_eau_rap: Optional[List[str]] = None
    noms_masse_eau_rap: Optional[List[str]] = None
    urns_masse_eau_rap: Optional[List[str]] = None
    codes_masse_eau_edl: Optional[List[str]] = None
    noms_masse_eau_edl: Optional[List[str]] = None
    urns_masse_eau_edl: Optional[List[str]] = None
    codes_reseau: Optional[List[str]] = None
    noms_reseau: Optional[List[str]] = None
    uris_reseau: Optional[List[str]] = None
    codes_groupe_parametre: Optional[List[str]] = None
    noms_groupe_parametre: Optional[List[str]] = None
    uris_groupe_parametre: Optional[List[str]] = None


class StationNappeParams(BaseModel):
    """
    Query parameters for groundwater quality stations.
    see: https://hubeau.eaufrance.fr/page/api-qualite-nappes
    """

    bss_id: Optional[List[str]] = Field(None, description="BSS station code(s)")
    code_commune: Optional[List[str]] = Field(None, description="INSEE commune code(s)")
    num_departement: Optional[List[str]] = Field(None, description="Department code(s)")
    nom_region: Optional[List[str]] = Field(None, description="Region name(s)")
    code_entite_hg_bdlisa: Optional[List[str]] = Field(
        None, description="BDLISA hydrogeological entity code(s)"
    )
    code_masse_eau_edl: Optional[List[str]] = Field(
        None, description="Water body code(s) EDL"
    )
    code_masse_eau_rap: Optional[List[str]] = Field(
        None, description="Water body code(s) RAP"
    )
    prof_invest_min: Optional[float] = Field(
        None, description="Min investigation depth (m)"
    )
    prof_invest_max: Optional[float] = Field(
        None, description="Max investigation depth (m)"
    )
    date_min_maj: Optional[str] = Field(
        None, description="Min update date (yyyy-MM-dd)"
    )
    date_max_maj: Optional[str] = Field(
        None, description="Max update date (yyyy-MM-dd)"
    )
    size: Optional[int] = Field(None, ge=1, le=20000)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")


class AnalyseNappeParams(BaseModel):
    """
    Query parameters for groundwater quality analyses.
    see: https://hubeau.eaufrance.fr/page/api-qualite-nappes
    """

    bss_id: Optional[List[str]] = Field(None, description="BSS station code(s)")
    code_param: Optional[List[int]] = Field(None, description="Parameter code(s)")
    code_fraction: Optional[List[int]] = Field(None, description="Fraction code(s)")
    code_groupe_parametre: Optional[List[str]] = Field(
        None, description="Parameter group code(s)"
    )
    code_qualification: Optional[List[str]] = Field(
        None, description="Qualification code(s)"
    )
    code_statut_analyse: Optional[List[str]] = Field(
        None, description="Analysis status code(s)"
    )
    code_region: Optional[List[str]] = Field(None, description="Region code(s)")
    num_departement: Optional[List[str]] = Field(None, description="Department code(s)")
    code_insee_actuel: Optional[List[str]] = Field(
        None, description="INSEE commune code(s)"
    )
    code_masse_eau_edl: Optional[List[str]] = Field(
        None, description="Water body code(s) EDL"
    )
    code_bassin_dce: Optional[List[str]] = Field(None, description="DCE basin code(s)")
    date_debut_prelevement: Optional[str] = Field(
        None, description="Start date (yyyy-MM-dd)"
    )
    date_fin_prelevement: Optional[str] = Field(
        None, description="End date (yyyy-MM-dd)"
    )
    date_min_maj: Optional[str] = Field(
        None, description="Min update date (yyyy-MM-dd)"
    )
    date_max_maj: Optional[str] = Field(
        None, description="Max update date (yyyy-MM-dd)"
    )
    resultat_min: Optional[float] = Field(None, description="Min result value")
    resultat_max: Optional[float] = Field(None, description="Max result value")
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("asc", pattern="^(asc|desc)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = Field(None, description="Search radius in km")

    model_config = ConfigDict(extra="allow")
