import pathlib
from dotenv import dotenv_values

from tests.integration.feature_repos.integration_test_repo_config import (
    IntegrationTestRepoConfig,
)


HERE = pathlib.Path(__file__).parent.absolute()
config = dotenv_values(HERE / ".env")
ASTRA_DB_SECURE_CONNECT_BUNDLE = config["ASTRA_DB_SECURE_CONNECT_BUNDLE"]
ASTRA_DB_USERNAME = config["ASTRA_DB_USERNAME"]
ASTRA_DB_PASSWORD = config["ASTRA_DB_PASSWORD"]
ASTRA_DB_KEYSPACE = config["ASTRA_DB_KEYSPACE"]


ASTRA_DB_CONFIG = {
    "type": ("feast_cassandra_online_store.cassandra_online_store"
             ".CassandraOnlineStore"),
    "secure_bundle_path": ASTRA_DB_SECURE_CONNECT_BUNDLE,
    "username": ASTRA_DB_USERNAME,
    "password": ASTRA_DB_PASSWORD,
    "keyspace": ASTRA_DB_KEYSPACE,
    "protocol_version": 4,
}

FULL_REPO_CONFIGS = [
    IntegrationTestRepoConfig(online_store=ASTRA_DB_CONFIG),
]
