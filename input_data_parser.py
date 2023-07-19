from cargo_space import CargoSpace
from dto import Params
from math import sqrt
from pydantic import BaseModel


class Cargo(BaseModel):
    width: int
    height: int
    length: int
    stacking: bool
    turnover: bool
    count: int


class Group(BaseModel):
    cargoes: list[Cargo]


class InputData(BaseModel):
    cargo_spaces: list[int]
    groups: list[Group]


class Input(BaseModel):
    input_data: InputData


class InputDataParser:
    def __init__(self, cargo_space: CargoSpace):
        self.__cargo_space: CargoSpace = cargo_space

    def get_params(self, json_data: dict) -> Params:
        inp = Input(**json_data)
        params = Params()
        cargo_space_id = inp.input_data.cargo_spaces[0]
        cargo_space = self.__cargo_space.get(cargo_space_id)
        params.type = cargo_space.cargo_space_type
        params.loading_width = cargo_space.width
        params.loading_height = cargo_space.height
        params.loading_length = cargo_space.length
        width_sum = 0
        height_sum = 0
        length_sum = 0
        volume_sum = 0
        for group in inp.input_data.groups:
            for cargo in group.cargoes:
                params.amount_of_cargoes += 1
                params.count_of_cargoes += cargo.count

                if params.min_cargo_width == 0 or cargo.width < params.min_cargo_width:
                    params.min_cargo_width = cargo.width
                if params.min_cargo_height == 0 or cargo.height < params.min_cargo_height:
                    params.min_cargo_height = cargo.height
                if params.min_cargo_length == 0 or cargo.length < params.min_cargo_length:
                    params.min_cargo_length = cargo.length

                params.max_cargo_width = max(params.max_cargo_width, cargo.width)
                params.max_cargo_height = max(params.max_cargo_height, cargo.height)
                params.max_cargo_length = max(params.max_cargo_length, cargo.length)

                width_sum += cargo.count * cargo.width
                height_sum += cargo.count * cargo.height
                length_sum += cargo.count * cargo.length

                volume = cargo.width * cargo.height * cargo.length
                if params.min_volume == 0 or volume < params.min_volume:
                    params.min_volume = volume
                params.max_volume = max(params.max_volume, volume)

                volume_sum += cargo.count * volume

                if not cargo.stacking:
                    params.not_stacking_cargo_volume += cargo.count * volume

                if cargo.stacking:
                    params.total_stacking += cargo.count
                if cargo.turnover:
                    params.total_turnover += cargo.count
                if not cargo.stacking and not cargo.turnover:
                    params.not_stacking_not_turnover += cargo.count
                if not cargo.stacking and cargo.turnover:
                    params.not_stacking_turnover += cargo.count
                if cargo.stacking and not cargo.turnover:
                    params.stacking_not_turnover += cargo.count
                if cargo.stacking and cargo.turnover:
                    params.stacking_turnover += cargo.count

        params.avg_cargo_width = width_sum / params.count_of_cargoes
        params.avg_cargo_height = height_sum / params.count_of_cargoes
        params.avg_cargo_length = length_sum / params.count_of_cargoes
        params.avg_volume = volume_sum / params.count_of_cargoes

        if params.count_of_cargoes == 1:
            return params

        diff_width = 0.0
        diff_height = 0.0
        diff_length = 0.0
        diff_volume = 0.0
        for group in inp.input_data.groups:
            for cargo in group.cargoes:
                diff_width += cargo.count * (cargo.width - params.avg_cargo_width) ** 2
                diff_height += cargo.count * (cargo.height - params.avg_cargo_height) ** 2
                diff_length += cargo.count * (cargo.length - params.avg_cargo_length) ** 2
                volume = cargo.width * cargo.height * cargo.length
                diff_volume += cargo.count * (volume - params.avg_volume) ** 2
        params.stdev_cargo_width = sqrt(diff_width / (params.count_of_cargoes - 1))
        params.stdev_cargo_height = sqrt(diff_height / (params.count_of_cargoes - 1))
        params.stdev_cargo_length = sqrt(diff_length / (params.count_of_cargoes - 1))
        params.stdev_cargo_volume = sqrt(diff_volume / (params.count_of_cargoes - 1))

        return params

