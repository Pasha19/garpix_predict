from dataclasses import dataclass
from pydantic import BaseModel


class CargoSpaceResponseResult(BaseModel):
    id: int
    cargo_space_type: str
    width: int
    height: int
    length: int


class CargoSpaceResponse(BaseModel):
    next: str | None
    results: list[CargoSpaceResponseResult]


@dataclass
class Params:
    type: str = ''
    loading_width: int = 0
    loading_height: int = 0
    loading_length: int = 0
    amount_of_cargoes: int = 0
    count_of_cargoes: int = 0
    min_cargo_width: int = 0
    min_cargo_height: int = 0
    min_cargo_length: int = 0
    max_cargo_width: int = 0
    max_cargo_height: int = 0
    max_cargo_length: int = 0
    avg_cargo_width: float = 0.0
    avg_cargo_height: float = 0.0
    avg_cargo_length: float = 0.0
    stdev_cargo_width: float = 0.0
    stdev_cargo_height: float = 0.0
    stdev_cargo_length: float = 0.0
    min_volume: int = 0
    max_volume: int = 0
    avg_volume: int = 0
    stdev_cargo_volume: float = 0.0
    not_stacking_cargo_volume: int = 0
    total_stacking: int = 0
    total_turnover: int = 0
    not_stacking_not_turnover: int = 0
    not_stacking_turnover: int = 0
    stacking_not_turnover: int = 0
    stacking_turnover: int = 0
