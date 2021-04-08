from requests import get
import json

url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'


def main():
    with open('data.txt', 'w') as f:
        arr = []
        for year in range(1970, 2020):
            for month in range(1, 12):
                _month1 = month if month > 9 else f'0{month}'
                _month2 = month + 1 if month > 8 else f'0{month+1}'
                params = {
                    'format': 'geojson',
                    'starttime': f'{year}-{_month1}-01',
                    'endtime': f'{year}-{_month2}-01',
                    'minmagnitude': '2'
                }
                res = get(url, params=params)
                data = res.json()
                arr = arr + data['features']
                print(f'{year}-{month}')
        f.write(json.dumps(arr))


main()
