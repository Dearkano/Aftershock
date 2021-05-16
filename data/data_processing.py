import numpy as np
import pandas as pd

DAY = 86400 * 1000
WEEK = DAY * 7
MONTH = DAY * 30
OFFSET = 5 # Coordinate offset


def adjust_structure(data):
    """
    Adjust the structure of the data so all fields are in the same layer. Changes made in place.
    Args:
        data (list): data to modify
    Returns:
        None
    """
    for i in range(len(data)):
        properties = {}
        for prop in data[i]['properties']:
            properties[prop] = data[i]['properties'][prop]
        properties['longitude'], properties['latitude'], properties['depth'] = data[i]['geometry']['coordinates']
        data[i] = properties

def count_foreshocks(stub, data):
    """
    Append number of foreshocks in the past 7 days for quakes with mag > 5, changes made in place.
    Args:
        stub (CosmosStub): stub to access Cosmos DB container
        data (list): current data
    Returns:
        None
    """
    # Only count foreshocks for earthquake with mag > 5
    for i in range(len(data)):
        if data[i]['mag'] >= 5:
            ts = data[i]['time']
            s_long, s_lat = data[i]['longitude'], data[i]['latitude']
            # Count # of foreshocks in current dataset
            j = i - 1
            n_foreshocks = 0
            while j >= 0 and data[j]['time'] >= ts - WEEK:
                long, lat = data[j]['longitude'], data[j]['latitude']
                if s_long - OFFSET <= long <= s_long + OFFSET and s_lat - OFFSET <= lat <= s_lat + OFFSET:
                    n_foreshocks += 1
                j -= 1

            # Query Cosmos DB
            query = 'SELECT value COUNT(1) FROM c WHERE c.time > {} AND c.time < {} AND c.longitude > {} AND c.longitude < {} AND c.latitude > {} AND c.latitude < {}'.format(
                ts - WEEK,
                ts,
                s_long - OFFSET,
                s_long + OFFSET,
                s_lat - OFFSET,
                s_lat + OFFSET
            )
            for count in stub.query_items(query):
                n_foreshocks += count
                break
            data[i]['n_foreshocks'] = n_foreshocks

def label(data):
    # Earthquakes with mag >= 5 are treated as training samples
    samples = []
    for i in range(len(data)):
        if data[i]['properties']['mag'] >= 5:
            samples.append((i, data[i]))
    
    x, y = [], []
    for i, sample in samples:
        counter = [0] * 9
        ts = sample['properties']['time']
        s_long, s_lat, _ = sample['geometry']['coordinates']
        # Ignore unusable samples
        if data[-1]['properties']['time'] < ts + MONTH:
            break
        # Otherwise do day/week/month labeling
        j = i + 1
        while data[j]['properties']['time'] <= ts + MONTH:
            long, lat, _ = data[j]['geometry']['coordinates']
            time = data[j]['properties']['time']
            mag = data[j]['properties']['mag']
            # If quake is in range
            if s_long - OFFSET <= long <= s_long + OFFSET and s_lat - OFFSET <= lat <= s_lat + OFFSET:
                if time <= ts + DAY:
                    if mag < 3:
                        counter[0] += 1
                    elif mag < 5:
                        counter[1] += 1
                    else:
                        counter[2] += 1
                if time <= ts + WEEK:
                    if mag < 3:
                        counter[3] += 1
                    elif mag < 5:
                        counter[4] += 1
                    else:
                        counter[5] += 1 
                if time <= ts + MONTH:
                    if mag < 3:
                        counter[6] += 1
                    elif mag < 5:
                        counter[7] += 1
                    else:
                        counter[8] += 1
            j += 1
        x.append(sample)
        y.append(counter)
    return x, y

def preprocess(x, y):
    x_arr = []
    for item in x:
        mag = item['properties']['mag']
        mmi = item['properties']['mmi']
        sig = item['properties']['sig']
        depth = item['geometry']['coordinates'][-1]
        n_foreshocks = item['n_foreshocks']
        x_arr.append([mag, mmi, sig, depth, n_foreshocks])
    x_arr = np.array(x_arr)
    x_df = pd.DataFrame(x_arr, columns=['mag', 'mmi', 'sig', 'depth', 'num_foreshocks'])
    # Fix missing values with mean
    x_df = x_df.fillna(x_df.mean())
    y_arr = np.array(y)
    y_df = pd.DataFrame(y_arr, columns=['day_mag12', 'day_mag34', 'day_mag5+', 
                                        'week_mag12', 'week_mag34', 'week_mag5+',
                                        'month_mag12', 'month_mag34', 'month_mag5+'])
    
    return x_df, y_df

if __name__ == '__main__':
    pass
