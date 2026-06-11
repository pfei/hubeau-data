from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Reseau(BaseModel):
    code: Optional[str] = None
    nom: Optional[str] = None
    debit: Optional[str] = None


class ResultatEauPotable(BaseModel):
    reseaux: Optional[List[Reseau]] = None
    code_departement: Optional[str] = None
    nom_departement: Optional[str] = None
    code_prelevement: Optional[str] = None
    code_parametre: Optional[str] = None
    code_parametre_se: Optional[str] = None
    code_parametre_cas: Optional[str] = None
    libelle_parametre: Optional[str] = None
    libelle_parametre_maj: Optional[str] = None
    libelle_parametre_web: Optional[str] = None
    code_type_parametre: Optional[str] = None
    code_lieu_analyse: Optional[str] = None
    reference_analyse: Optional[str] = None
    resultat_alphanumerique: Optional[str] = None
    resultat_numerique: Optional[float] = None
    libelle_unite: Optional[str] = None
    code_unite: Optional[str] = None
    limite_qualite_parametre: Optional[str] = None
    reference_qualite_parametre: Optional[str] = None
    code_commune: Optional[str] = None
    nom_commune: Optional[str] = None
    nom_uge: Optional[str] = None
    nom_distributeur: Optional[str] = None
    nom_moa: Optional[str] = None
    code_installation_amont: Optional[str] = None
    nom_installation_amont: Optional[str] = None
    date_prelevement: Optional[str] = None
    conclusion_conformite_prelevement: Optional[str] = None
    conformite_limites_bact_prelevement: Optional[str] = None
    conformite_limites_pc_prelevement: Optional[str] = None
    conformite_references_bact_prelevement: Optional[str] = None
    conformite_references_pc_prelevement: Optional[str] = None


class CommuneUdi(BaseModel):
    annee: Optional[str] = None
    code_commune: Optional[str] = None
    code_reseau: Optional[str] = None
    debut_alim: Optional[str] = None
    nom_commune: Optional[str] = None
    nom_quartier: Optional[str] = None
    nom_reseau: Optional[str] = None


class ResultatEauPotableParams(BaseModel):
    """Query parameters for drinking water analysis results."""

    code_commune: Optional[List[str]] = Field(None, description="Commune code(s) INSEE")
    code_departement: Optional[List[str]] = Field(
        None, description="Department code(s)"
    )
    code_reseau: Optional[List[str]] = Field(
        None, description="Network code(s) SISE-Eaux"
    )
    code_parametre: Optional[List[str]] = Field(
        None, description="Parameter code(s) Sandre"
    )
    code_parametre_se: Optional[List[str]] = Field(
        None, description="Parameter code(s) SISE-Eaux"
    )
    code_lieu_analyse: Optional[str] = Field(
        None, description="Analysis location: T (terrain) or L (laboratoire)"
    )
    date_min_prelevement: Optional[str] = Field(
        None, description="Min sampling date (YYYY-MM-DD)"
    )
    date_max_prelevement: Optional[str] = Field(
        None, description="Max sampling date (YYYY-MM-DD)"
    )
    conformite_limites_bact_prelevement: Optional[str] = Field(
        None, description="Bacteriological conformity: C/N/D/S"
    )
    conformite_limites_pc_prelevement: Optional[str] = Field(
        None, description="Chemical conformity: C/N/D/S"
    )
    borne_inf_resultat: Optional[float] = Field(None, description="Min numeric result")
    borne_sup_resultat: Optional[float] = Field(None, description="Max numeric result")
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("desc", pattern="^(asc|desc)$")

    model_config = ConfigDict(extra="allow")


class CommuneUdiParams(BaseModel):
    """Query parameters for UDI-commune links."""

    code_commune: Optional[List[str]] = Field(None, description="Commune code(s) INSEE")
    code_reseau: Optional[List[str]] = Field(
        None, description="Network code(s) SISE-Eaux"
    )
    nom_commune: Optional[List[str]] = Field(None, description="Commune name(s)")
    nom_reseau: Optional[List[str]] = Field(None, description="Network name(s)")
    annee: Optional[List[str]] = Field(None, description="Year(s) (max 10)")
    size: Optional[int] = Field(None, ge=1, le=20000)
    sort: Optional[str] = Field("asc", pattern="^(asc|desc)$")

    model_config = ConfigDict(extra="allow")
