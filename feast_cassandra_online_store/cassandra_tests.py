import pathlib
from dotenv import dotenv_values

from tests.integration.feature_repos.integration_test_repo_config import (
    IntegrationTestRepoConfig,
)


HERE = pathlib.Path(__file__).parent.absolute()
config = dotenv_values(HERE / '.env')
CASSANDRA_HOSTS = config['CASSANDRA_HOSTS']
CASSANDRA_KEYSPACE = config['CASSANDRA_KEYSPACE']
CASSANDRA_PORT = config.get('CASSANDRA_PORT')
CASSANDRA_USERNAME = config.get('CASSANDRA_USERNAME')
CASSANDRA_PASSWORD = config.get('CASSANDRA_PASSWORD')

if CASSANDRA_HOSTS:
    hosts = CASSANDRA_HOSTS.split(',')
else:
    hosts = None
if CASSANDRA_PORT:
    port = int(CASSANDRA_PORT)
else:
    port = None


CASSANDRA_CONFIG = {
    k: v
    for k, v in {
        "type": "feast_cassandra_online_store.cassandra_online_store.CassandraOnlineStore",
        "hosts": hosts,
        "port": port,
        "keyspace": CASSANDRA_KEYSPACE,
        "username": CASSANDRA_USERNAME,
        "password": CASSANDRA_PASSWORD,
    }.items()
    if v is not None
}


FULL_REPO_CONFIGS = [
    IntegrationTestRepoConfig(online_store=CASSANDRA_CONFIG),
]
