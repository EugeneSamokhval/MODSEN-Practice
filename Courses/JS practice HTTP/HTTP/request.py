import requests


def main():
    content = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?id=625143&appid=8db44f8b758f996a9139941aa44f6877"
    )
    data_dict = content.json()

    for key in data_dict.keys():
        print(key, "=", data_dict.get(key))


main()
