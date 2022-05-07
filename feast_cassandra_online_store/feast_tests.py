from tests.integration.feature_repos.integration_test_repo_config import (
    IntegrationTestRepoConfig,
)

CASSANDRA_CONFIG = {
    "type": "feast_cassandra_online_store.cassandra_online_store.CassandraOnlineStore",
    "hosts": ["172.18.0.2"],
    # "secure_bundle_path": "",
    # "port": "",
    "keyspace": "feastks",
    # "username": "",
    # "password": "",
}

FULL_REPO_CONFIGS = [
    IntegrationTestRepoConfig(online_store=CASSANDRA_CONFIG),
]