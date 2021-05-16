from hashlib import sha1
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceNotFoundError, CosmosResourceExistsError

URL = 'https://5412fpcosmos.documents.azure.com:443/'
API_KEY = 'V2LKYVNjlhNEkBlBXCERvSeaSzsscxNelITslUxJ57ehplxXRKa2wlqKJJh64ZHS2Sv7lIX4RdQarStJgjZlIw=='
client = CosmosClient(URL, API_KEY)


class CosmosStub:
    def __init__(self, db, container_name, partition_key):
        self.db = db
        self.container_name = container_name
        self.partition_key = partition_key
        try:
            self.container = db.create_container(
                id=container_name,
                partition_key=PartitionKey(path='/{}'.format(partition_key))
            )
        except CosmosResourceExistsError:
            print('Container already exists, use the existing container.')
            self.container = db.get_container_client(container_name)

    @staticmethod
    def hash64(value):
        # Cosmos expects Json-serializable format, use int instead of bytes
        return str(int.from_bytes(sha1(value.encode('utf-8')).digest()[:8], byteorder='big'))

    @staticmethod
    def get_partition_key(value):
        return int(value) % 5

    def create(self, id_, body):
        """
        Create a new entry in Cosmos DB
        Args: 
            id_ (str): unique identifier of this entry
            body (dict): the body of the entry
        Returns:
            True/False: indicate success/failure
        """
        key = CosmosStub.hash64(id_)
        body['id'] = key
        body[self.partition_key] = CosmosStub.get_partition_key(key)
        try:
            self.container.create_item(body)
        except CosmosResourceExistsError:
            print('Cosmos key exists in the container, skipped.')
            return False
        return True

    def read(self, id_):
        """
        Return an entry by its cosmos key
        Args: 
            id_ (str): unique identifier of this entry
        Returns:
            body (dict): body of the entry, None if not found
        """
        key = CosmosStub.hash64(id_)
        try:
            body = self.container.read_item(
                key, CosmosStub.get_partition_key(key))
            return body
        except CosmosResourceNotFoundError:
            print('Entry not found')
            return None

    def delete(self, id_):
        """
        Delete an entry
        Args: 
            id_ (str): unique identifier of this entry
        Returns:
            True/False: indicate success/failure
        """
        key = CosmosStub.hash64(id_)
        try:
            self.container.delete_item(key, CosmosStub.get_partition_key(key))
            return True
        except CosmosResourceNotFoundError:
            return False

    def query_items(self, query, cross_paritition=True):
        """
        Return entries using SQL query
        Args: 
            query (str): SQL query
        Returns:
            tt (iterator): retrieved records
        """
        return self.container.query_items(query=query, enable_cross_partition_query=cross_paritition)

    # Update is not supported, use delete + create instead
