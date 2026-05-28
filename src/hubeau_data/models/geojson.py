from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

# --- GeoJSON/Spatial Models ---

LngLat = List[float]  # [longitude, latitude]
LngLatAlt = List[float]  # [longitude, latitude, altitude] (if present)


class CrsProperties(BaseModel):
    name: str


class Crs(BaseModel):
    type: str  # Usually "name"
    properties: CrsProperties


class Point(BaseModel):
    type: str  # "Point"
    coordinates: LngLat


class MultiPoint(BaseModel):
    type: str  # "MultiPoint"
    coordinates: List[LngLat]


class LineString(BaseModel):
    type: str  # "LineString"
    coordinates: List[LngLat]


class MultiLineString(BaseModel):
    type: str  # "MultiLineString"
    coordinates: List[List[LngLat]]


class Polygon(BaseModel):
    type: str  # "Polygon"
    coordinates: List[List[LngLat]]


class MultiPolygon(BaseModel):
    type: str  # "MultiPolygon"
    coordinates: List[List[List[LngLat]]]


class GeometryCollection(BaseModel):
    type: str  # "GeometryCollection"
    geometries: List[
        Union[
            "Point",
            "MultiPoint",
            "LineString",
            "MultiLineString",
            "Polygon",
            "MultiPolygon",
        ]
    ]


Geometry = Union[
    Point,
    MultiPoint,
    LineString,
    MultiLineString,
    Polygon,
    MultiPolygon,
    GeometryCollection,
]


class Feature(BaseModel):
    type: str  # "Feature"
    bbox: Optional[List[float]] = None
    crs: Optional[Crs] = None
    geometry: Optional[Geometry] = None
    id: Optional[Union[str, int]] = None
    properties: Optional[Dict[str, Any]] = None


class FeatureCollection(BaseModel):
    type: str  # "FeatureCollection"
    features: List[Feature]
    bbox: Optional[List[float]] = None
    crs: Optional[Crs] = None
