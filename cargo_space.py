from dto import CargoSpaceResponseResult


class CargoSpace:
    def __init__(self):
        self.__data: dict[int, CargoSpaceResponseResult] = {}

    def add(self, cargo_space: CargoSpaceResponseResult) -> None:
        if cargo_space.id in self.__data:
            raise RuntimeError(f"cargo space {cargo_space.id} already exists")
        self.__data[cargo_space.id] = cargo_space

    def get(self, cargo_space_id: int) -> CargoSpaceResponseResult:
        if cargo_space_id not in self.__data:
            raise RuntimeError(f"cargo space {cargo_space_id} not found")
        return self.__data[cargo_space_id]
