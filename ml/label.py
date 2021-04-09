import math
import json
rec = {}
out = []
minlatitude = 32
maxlatitude = 42
maxlongitude = -114
minlongitude = -125
delta = 31515000000


def getLocationKey(lat, lon):
    max_lat = math.ceil(lat)
    max_lon = math.ceil(lon)
    return f'{max_lat-1}|{max_lat},{max_lon-1}|{max_lon}'


def main():
    for lat in range(minlatitude, maxlatitude + 1):
        for lon in range(minlongitude, maxlongitude + 1):
            rec[getLocationKey(lat, lon)] = []
    aftershock = 0
    not_aftershock = 0
    with open('CA.txt', 'r') as f:
        data = json.loads(f.read())
        with open('CA_labeled.txt', 'w') as f1:
            for item in data:
                lon, lat, depth = item['geometry']['coordinates']
                time = item['properties']['time']
                mag = item['properties']['mag']
                key = getLocationKey(lat, lon)
                arr = rec[key]
                while len(arr) > 0:
                    if time - arr[0]['properties']['time'] > delta:
                        arr.pop(0)
                    else:
                        break
                is_aftershock = False
                for p in arr:
                    if p['properties']['mag'] > mag:
                        is_aftershock = True
                        break
                arr.append(item)
                obj = {
                    'lon': lon,
                    'lat': lat,
                    'time': time,
                    'depth': depth,
                    'mag': mag,
                    'is_aftershock': is_aftershock,
                    'location': item['properties']['place'],
                    'title': item['properties']['title']
                }
                out.append(obj)
                if is_aftershock:
                    aftershock += 1
                else:
                    not_aftershock += 1
            print(aftershock, not_aftershock)
            f1.write(json.dumps(out))


main()
