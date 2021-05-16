from datetime import datetime
import json
import os
import sys
import time
from cosmos_stub import client, CosmosStub
from feed import get_current_feed
from data_processing import count_foreshocks, adjust_structure


CONFIG_PATH = '{}/feed_config.txt'.format(os.path.abspath(os.getcwd()))
QUERY_INTERVAL = 60

# Cosmos related macros
DB_NAME = 'db'
CONTAINER_NAME = 'usgs_earthquake'
PARTITION_KEY = 'partition'
db = client.get_database_client(DB_NAME)
stub = CosmosStub(db, CONTAINER_NAME, PARTITION_KEY) 

def run():
    """
    Continuously get data from USGS, at 1 minute interval by default
    Args: 
        None
    Returns:
        None
    """
    try:
        with open(CONFIG_PATH, 'r') as f:
            last_ts = json.loads(f.read())['last_ts']
    except FileNotFoundError:
        sys.exit('Config file not found, please provide one')

    while 1:
        last_ts, data = get_current_feed(last_ts)
        print('{} new entries retrieved from USGS'.format(len(data)))
        with open(CONFIG_PATH, 'w') as f:
            f.write(json.dumps({'last_ts': last_ts}))
        adjust_structure(data)
        data.sort(key=lambda x: x['time'])
        count_foreshocks(stub, data)
        # Add new data to CosmosDB
        for item in data:
            stub.create(item['ids'], item)
        print('Sleep for {} seconds'.format(QUERY_INTERVAL))
        time.sleep(QUERY_INTERVAL)


if __name__ == '__main__':
    run()
