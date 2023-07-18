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
