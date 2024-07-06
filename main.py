from iss_api_handler import IssAPIHandler
from sunrise_api_handler import SunriseAPIHandler
import datetime as dt
import time
import math
import smtplib


def main() -> None:
    user_data = read_user_data(USER_DATA_FILE)
    coordinates_data = read_coordinates(COORDINATES_FILE)

    sunrise_api_handler = SunriseAPIHandler(coordinates_data)

    sunrise_time = sunrise_api_handler.sunrise_time()
    sunset_time = sunrise_api_handler.sunset_time()

    current_position = (float(coordinates_data["lat"]), float(coordinates_data["lng"]))
    iss_position = IssAPIHandler.get_iss_position()

    while True:
        time.sleep(60)
        if is_evening(sunrise_time, sunset_time, coordinates_data["tzid"]) and is_iss_closeby(current_position, iss_position):
            send_email(user_data)


def read_coordinates(file_name: str) -> dict[str, str]:
    with open(file_name, "r", encoding="utf-8") as data_file:
        data = data_file.readlines()[1]
        split_data = data.strip().split(",")
        return {
            "lat": split_data[0],
            "lng": split_data[1],
            "formatted": 0,
            "tzid": split_data[2],
        }


def read_user_data(file_name: str) -> dict[str, str]:
    with open(file_name, "r", encoding="utf-8") as data_file:
        data = data_file.readlines()[1]
        split_data = data.strip().split(",")
        return {
            "name_to": split_data[0],
            "email_to": split_data[1],
            "email_from": split_data[2],
            "password_from": split_data[3],
        }


def is_evening(sunrise: tuple[int, int, int], sunset: tuple[int, int, int], timezone: str) -> bool:
    time_now = dt.datetime.now(dt.timezone.utc)
    today_date = time_now.date()

    sunrise_time = dt.datetime.combine(today_date, dt.time(*sunrise), dt.timezone.utc)
    sunset_time = dt.datetime.combine(today_date, dt.time(*sunset), dt.timezone.utc)

    return not (sunrise_time <= time_now < sunset_time)


def haversine(coord1: tuple[float, float], coord2: tuple[float, float]) -> float:
    R = 6371.0

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def is_iss_closeby(current_position: tuple[float, float], iss_position: tuple[float, float]) -> bool:
    distance = haversine(current_position, iss_position)
    return distance <= 100


def send_email(user_data: dict[str, str]) -> None:
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as conn:
            conn.starttls()
            conn.login(user=user_data["email_from"], password=user_data["password_from"])
            conn.sendmail(
                from_addr=user_data["email_from"],
                to_addrs=user_data["email_to"],
                msg=f"Subject: ISS Is near your location\n\n"
                    f"Dear {user_data['name_to']},\nThe ISS is in 100 km-s of your area. "
                    f"Look up to the sky, and you might spot it. :)\n\nPython App".encode("utf-8")
            )
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    COORDINATES_FILE: str = "./Data Files/coords.csv"
    USER_DATA_FILE: str = "./Data Files/user_data.csv"
    main()
