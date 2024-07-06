import requests


class IssAPIHandler:
    @staticmethod
    def get_iss_position() -> tuple[float, float]:
        response = requests.get("http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        data: dict = response.json()["iss_position"]

        return float(data["longitude"]), float(data["latitude"])