from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AchatSubstance(BaseModel):
    amm: Optional[str] = None
    annee: Optional[int] = None
    achat_etranger: Optional[str] = None
    classification: Optional[str] = None
    classification_mention: Optional[str] = None
    code_cas: Optional[str] = None
    code_substance: Optional[str] = None
    code_territoire: Optional[str] = None
    fonction: Optional[str] = None
    libelle_substance: Optional[str] = None
    libelle_territoire: Optional[str] = None
    quantite: Optional[float] = None
    type_territoire: Optional[str] = None
    uri_substance: Optional[str] = None
    uri_territoire: Optional[str] = None


class AchatProduit(BaseModel):
    achat_etranger: Optional[str] = None
    annee: Optional[int] = None
    amm: Optional[str] = None
    code_territoire: Optional[str] = None
    eaj: Optional[str] = None
    libelle_territoire: Optional[str] = None
    type_territoire: Optional[str] = None
    uri_territoire: Optional[str] = None
    quantite: Optional[float] = None
    unite: Optional[str] = None


class VenteSubstance(BaseModel):
    amm: Optional[str] = None
    annee: Optional[int] = None
    classification: Optional[str] = None
    classification_mention: Optional[str] = None
    code_cas: Optional[str] = None
    code_substance: Optional[str] = None
    code_territoire: Optional[str] = None
    fonction: Optional[str] = None
    libelle_substance: Optional[str] = None
    quantite: Optional[float] = None
    libelle_territoire: Optional[str] = None
    type_territoire: Optional[str] = None
    uri_substance: Optional[str] = None
    uri_territoire: Optional[str] = None


class VenteProduit(BaseModel):
    annee: Optional[int] = None
    amm: Optional[str] = None
    eaj: Optional[str] = None
    code_territoire: Optional[str] = None
    libelle_territoire: Optional[str] = None
    type_territoire: Optional[str] = None
    uri_territoire: Optional[str] = None
    quantite: Optional[float] = None
    unite: Optional[str] = None


class AchatSubstanceParams(BaseModel):
    """Query parameters for pesticide substance purchases."""

    type_territoire: Optional[str] = Field(
        "National",
        description="Territory type: Zone postale, Département, Région, National",
    )
    code_territoire: Optional[str] = Field(None, description="Territory code(s)")
    libelle_territoire: Optional[str] = Field(None, description="Territory label(s)")
    code_substance: Optional[str] = Field(None, description="Sandre substance code(s)")
    libelle_substance: Optional[str] = Field(None, description="Substance label(s)")
    code_cas: Optional[str] = Field(None, description="CAS code(s)")
    fonction: Optional[str] = Field(None, description="Substance function(s)")
    classification: Optional[str] = Field(None, description="Classification(s)")
    amm: Optional[str] = Field(None, description="AMM number(s)")
    achat_etranger: Optional[str] = Field(
        None, description="Foreign purchase: Oui/Non/nc"
    )
    annee_min: Optional[int] = Field(None, description="Min year")
    annee_max: Optional[int] = Field(None, description="Max year")
    quantite_min: Optional[float] = Field(None, description="Min quantity (kg)")
    quantite_max: Optional[float] = Field(None, description="Max quantity (kg)")
    size: Optional[int] = Field(None, ge=1)
    sort: Optional[str] = Field("desc", pattern="^(asc|desc)$")

    model_config = ConfigDict(extra="allow")


class AchatProduitParams(BaseModel):
    """Query parameters for pesticide product purchases."""

    type_territoire: Optional[str] = Field(
        "National",
        description="Territory type: Zone postale, Département, Région, National",
    )
    code_territoire: Optional[str] = Field(None, description="Territory code(s)")
    libelle_territoire: Optional[str] = Field(None, description="Territory label(s)")
    amm: Optional[str] = Field(None, description="AMM number(s)")
    achat_etranger: Optional[str] = Field(
        None, description="Foreign purchase: Oui/Non/nc"
    )
    eaj: Optional[str] = Field(None, description="Garden use authorized: Oui/Non/nc")
    unite: Optional[str] = Field(None, description="Unit: l or kg")
    annee_min: Optional[int] = Field(None, description="Min year")
    annee_max: Optional[int] = Field(None, description="Max year")
    quantite_min: Optional[float] = Field(None, description="Min quantity")
    quantite_max: Optional[float] = Field(None, description="Max quantity")
    size: Optional[int] = Field(None, ge=1)
    sort: Optional[str] = Field("desc", pattern="^(asc|desc)$")

    model_config = ConfigDict(extra="allow")


class VenteSubstanceParams(BaseModel):
    """Query parameters for pesticide substance sales."""

    type_territoire: Optional[str] = Field(
        "National", description="Territory type: Département, Région, National"
    )
    code_territoire: Optional[str] = Field(None, description="Territory code(s)")
    libelle_territoire: Optional[str] = Field(None, description="Territory label(s)")
    code_substance: Optional[str] = Field(None, description="Sandre substance code(s)")
    libelle_substance: Optional[str] = Field(None, description="Substance label(s)")
    code_cas: Optional[str] = Field(None, description="CAS code(s)")
    fonction: Optional[str] = Field(None, description="Substance function(s)")
    classification: Optional[str] = Field(None, description="Classification(s)")
    amm: Optional[str] = Field(None, description="AMM number(s)")
    annee_min: Optional[int] = Field(None, description="Min year")
    annee_max: Optional[int] = Field(None, description="Max year")
    quantite_min: Optional[float] = Field(None, description="Min quantity (kg)")
    quantite_max: Optional[float] = Field(None, description="Max quantity (kg)")
    size: Optional[int] = Field(None, ge=1)
    sort: Optional[str] = Field("desc", pattern="^(asc|desc)$")

    model_config = ConfigDict(extra="allow")


class VenteProduitParams(BaseModel):
    """Query parameters for pesticide product sales."""

    type_territoire: Optional[str] = Field(
        "National", description="Territory type: Département, Région, National"
    )
    code_territoire: Optional[str] = Field(None, description="Territory code(s)")
    libelle_territoire: Optional[str] = Field(None, description="Territory label(s)")
    amm: Optional[str] = Field(None, description="AMM number(s)")
    eaj: Optional[str] = Field(None, description="Garden use authorized: Oui/Non")
    unite: Optional[str] = Field(None, description="Unit: l or kg")
    annee_min: Optional[int] = Field(None, description="Min year")
    annee_max: Optional[int] = Field(None, description="Max year")
    quantite_min: Optional[float] = Field(None, description="Min quantity")
    quantite_max: Optional[float] = Field(None, description="Max quantity")
    size: Optional[int] = Field(None, ge=1)
    sort: Optional[str] = Field("desc", pattern="^(asc|desc)$")

    model_config = ConfigDict(extra="allow")
