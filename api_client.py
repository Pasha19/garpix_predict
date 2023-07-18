from collections.abc import Generator
from dto import CargoSpaceResponse, CargoSpaceResponseResult
from requests import get, post


class ApiClient:
    def __init__(self, username: str, password: str, base: str = 'https://back.glsystem.net/api/v1'):
        self.__username: str = username
        self.__password: str = password
        self.__base: str = base
        self.__token: str | None = None
        self.__login()

    def __login(self) -> None:
        data = {
            'username': self.__username,
            'password': self.__password,
        }
        response = post(self.__base + '/auth/login/', data=data)
        response.raise_for_status()
        json_data = response.json()
        self.__token: str = json_data['access_token']

    def get_cargo_spaces(self) -> Generator[list[CargoSpaceResponseResult], None, None]:
        if self.__token is None:
            self.__login()
        auth = {'authorization': 'Bearer ' + self.__token}
        url = self.__base + '/cargo-space/?per_page=100'
        while True:
            response = get(url, headers=auth)
            response.raise_for_status()
            json_data = response.json()
            parsed = CargoSpaceResponse(**json_data)
            yield parsed.results
            if parsed.next is None:
                break
            url = parsed.next
