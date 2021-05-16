from requests import get
from datetime import datetime

# USGS query API: https://earthquake.usgs.gov/fdsnws/event/1/#parameters
URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query'

def get_current_feed(start_ts):
    """
    Get global earthquake data from starttime to present
    Args:
        start_ts (int): start timestamp
    Returns:
        present (int): current timestamp
        data (list): all earthquake entries
    """
    # Set chunk due to 20000 records per query limit
    chunk = 86400 * 50 
    present_ts = int(datetime.now().timestamp())
    ret = []
    while 1:
        endtime = datetime.fromtimestamp(min(start_ts + chunk, present_ts)).isoformat()
        params = {
            'format': 'geojson',
            'starttime': datetime.fromtimestamp(start_ts).isoformat(),
            'endtime': endtime,
            'minmagnitude': '1',
        }
        start_ts += chunk
        res = get(URL, params=params)
        if res.status_code != 200:
            continue
        data = res.json()['features']
        ret += data
        if start_ts > present_ts:
            break
    return present_ts, ret
