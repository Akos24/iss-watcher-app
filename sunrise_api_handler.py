import requests


class SunriseAPIHandler:
    def __init__(self, params: dict[str, str]):
        self.params = params

    def sunrise_time(self) -> tuple[int, int, int]:
        response = requests.get(url="https://api.sunrise-sunset.org/json", params=self.params)
        response.raise_for_status()

        data: str = response.json()["results"]["sunrise"]
        sunrise_list: list = data.split("T")[1].split("+")[0].split(":")

        hour: int = int(sunrise_list[0])
        minute: int = int(sunrise_list[1])
        second: int = int(sunrise_list[2])

        return hour, minute, second

    def sunset_time(self) -> tuple[int, int, int]:
        response = requests.get(url="https://api.sunrise-sunset.org/json", params=self.params)
        response.raise_for_status()

        data: str = response.json()["results"]["sunset"]
        sunset_list: list = data.split("T")[1].split("+")[0].split(":")

        hour: int = int(sunset_list[0])
        minute: int = int(sunset_list[1])
        second: int = int(sunset_list[2])

        return hour, minute, second
