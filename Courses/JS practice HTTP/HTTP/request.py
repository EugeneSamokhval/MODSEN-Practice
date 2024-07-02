import requests

# Чтобы получить 409 код нужно отправлять очень много запросов при ограничени в 60 запросов в минуту это невозможно
# Чтобы получить 300-399 коды нужно обратиться к перенесённому сайту
# Код коды от 100 до 199 являються промежуточными и поэтому они при обычных запросах не отображаються
# Код 500 можно получить только при внутренней ошибке сервера
api_keys = [
    "http://api.openweathermap.org/data/2.5/weather?id=625143&appid=8db44f8b758f996a9139941aa44f6877",
    "http://api.openweathermap.org/data/2.5/weather?id=625143&appid=8",
    "http://api.openweathermap.org/data/2.5/weather?id=-1&appid=8db44f8b758f996a9139941aa44f6877",
    "http://api.openweathermap.org/dadsd/appid=8db44f8b758f996a9139941aa44f6877",
]


def main():
    unique_codes = set()
    for key in api_keys:
        content = requests.get(key)
        if content.status_code == 200:
            data_dict = content.json()

            for key in data_dict.keys():
                print(key, "=", data_dict.get(key))
        else:
            print("Got status code:", content.status_code)
    for i in range(250):
        content = requests.get(api_keys[0])
        unique_codes.add(content.status_code)
    for code in unique_codes:
        print(code)


main()
