from api_client import ApiClient
from cargo_space import CargoSpace
from dotenv import load_dotenv
from input_data_parser import InputDataParser
import json
from os import getenv
from predictor import Predictor
from sys import argv


def main(filename: str):
    garpix_api_username = getenv('GARPIX_API_USERNAME')
    garpix_api_password = getenv('GARPIX_API_PASSWORD')
    client = ApiClient(garpix_api_username, garpix_api_password)
    cargo_spaces = CargoSpace()
    for spaces in client.get_cargo_spaces():
        for space in spaces:
            cargo_spaces.add(space)
    with open(filename, 'r') as file:
        json_input: dict = json.load(file)
    if type(json_input) is not dict:
        raise RuntimeError('failed to parse input')
    input_data_parser = InputDataParser(cargo_spaces)
    params = input_data_parser.get_params(json_input)
    predictor = Predictor('finalized_model_RF.sav', 'finalized_scaler.sav', 'finalized_le.sav')
    density_percent = predictor.predict_density_percent(params)
    print(json.dumps({'density_percent': density_percent}, indent=4))


if __name__ == '__main__':
    load_dotenv()
    main(argv[1])
