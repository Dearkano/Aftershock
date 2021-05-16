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


def arrangeDataByGrid():
    for lat in range(minlatitude, maxlatitude + 1):
        for lon in range(minlongitude, maxlongitude + 1):
            rec[getLocationKey(lat, lon)] = []

    with open('CA.txt', 'r') as f:
        data = json.loads(f.read())
        for item in data:
            lon, lat, depth = item['geometry']['coordinates']
            key = getLocationKey(lat, lon)
            arr = rec[key]
            arr.append(item)


def main():
    aftershock = 0
    not_aftershock = 0
    arrangeDataByGrid()
    for i, v in rec.items():
        print(f'key: {i}, len={len(v)}')
    with open('CA_labeled.txt', 'w') as f:
        for key, arr in rec.items():
            print(key)
            for i, item in enumerate(arr):
                lon, lat, depth = item['geometry']['coordinates']
                time = item['properties']['time']
                mag = item['properties']['mag']

                pre = []
                idx = i - 1
                time = item['properties']['time']
                while idx >= 0:
                    if time - arr[idx]['properties']['time'] < delta:
                        pre.insert(0, arr[idx])
                        idx -= 1
                    else:
                        break

                after = []
                idx = i + 1
                while idx < len(arr):
                    if arr[idx]['properties']['time'] - time < delta:
                        after.append(arr[idx])
                    idx += 1

                # calculate the probability
                features = []
                labels = []
                m = 2.0
                while m <= 9.0:
                    features.append(
                        0 if len(pre) == 0 else len(list(filter(lambda x: x['properties']['mag'] > m, pre)))/len(pre))
                    m += 0.1

                m = 2.0
                while m <= 9.0:
                    labels.append(
                        0 if len(after) == 0 else len(list(filter(lambda x: x['properties']['mag'] > m, after)))/len(after))
                    m += 1

                obj = {
                    'lon': lon,
                    'lat': lat,
                    'time': time,
                    'depth': depth,
                    'mag': mag,
                    'features': features,
                    'labels': labels,
                    'location': item['properties']['place'],
                    'title': item['properties']['title']
                }

                out.append(obj)
        print('finish')
        f.write(json.dumps(out))


main()
