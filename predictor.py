from dto import Params
from pandas import DataFrame
from pickle import load


class Predictor:
    COLUMN_NAMES = [
        'type',
        'amount_of_cargoes', 'count_of_cargoes',
        'loading_width', 'loading_height', 'loading_length',
        'min_cargo_width', 'min_cargo_height', 'min_cargo_length',
        'max_cargo_width', 'max_cargo_height', 'max_cargo_length',
        'average_cargo_width', 'average_cargo_height', 'average_cargo_length',
        'stdev_cargo_width', 'stdev_cargo_height', 'stdev_cargo_length',
        'min_cargo_volume', 'max_cargo_volume', 'average_cargo_volume', 'stdev_cargo_volume',
        'not_stacking_cargo_volume',
        'total_stacking', 'total_turnover',
        'not_stacking_not_turnover',
        'not_stacking_turnover',
        'stacking_not_turnover',
        'stacking_turnover',
    ]

    def __init__(self, filename_model: str, filename_scaler: str, filename_le: str):
        with open(filename_model, 'rb') as file:
            self.__model = load(file)
        with open(filename_scaler, 'rb') as file:
            self.__scaler = load(file)
        with open(filename_le, 'rb') as file:
            self.__le = load(file)

    def predict_density_percent(self, params: Params) -> float:
        params_list = [
            params.type,
            params.amount_of_cargoes, params.count_of_cargoes,
            params.loading_width, params.loading_height, params.loading_length,
            params.min_cargo_width, params.min_cargo_height, params.min_cargo_length,
            params.max_cargo_width, params.max_cargo_height, params.max_cargo_length,
            params.avg_cargo_width, params.avg_cargo_height, params.avg_cargo_length,
            params.stdev_cargo_width, params.stdev_cargo_height, params.stdev_cargo_length,
            params.min_volume, params.max_volume, params.avg_volume, params.stdev_cargo_volume,
            params.not_stacking_cargo_volume,
            params.total_stacking, params.total_turnover,
            params.not_stacking_not_turnover,
            params.not_stacking_turnover,
            params.stacking_not_turnover,
            params.stacking_turnover,
        ]
        data_frame = DataFrame([params_list], columns=self.COLUMN_NAMES)
        data_frame.iloc[:, 1:] = DataFrame(
            self.__scaler.transform(data_frame.iloc[:, 1:]),
            columns=self.COLUMN_NAMES[1:],
        )
        data_frame['type'] = self.__le.transform(data_frame['type'])
        return self.__model.predict(data_frame)[0]
