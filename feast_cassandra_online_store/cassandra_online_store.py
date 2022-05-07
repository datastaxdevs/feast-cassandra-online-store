from datetime import datetime
from typing import Sequence, Union, List, Optional, Tuple, Dict, Callable, Any

import pytz
from feast import RepoConfig, FeatureView, Entity
from feast.infra.key_encoding_utils import serialize_entity_key
from feast.infra.online_stores.online_store import OnlineStore
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto

from feast.repo_config import FeastConfigBaseModel
from pydantic import StrictStr, StrictInt
from pydantic.typing import Literal

from cassandra.cluster import Cluster, Session
from cassandra.auth import PlainTextAuthProvider


class CassandraInvalidConfig(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


E_CASSANDRA_UNEXPECTED_CONFIGURATION_CLASS = "Unexpected configuration object (not a CassandraOnlineStoreConfig instance)"
E_CASSANDRA_NOT_CONFIGURED = "Inconsistent Cassandra configuration: provide exactly one between 'hosts' and 'secure_bundle_path' and a 'keyspace'"
E_CASSANDRA_MISCONFIGURED = "Inconsistent Cassandra configuration: provide either 'hosts or 'secure_bundle_path', not both"
E_CASSANDRA_INCONSISTENT_AUTH = "Username and password for Cassandra must be provided either both or none"

class CassandraOnlineStoreConfig(FeastConfigBaseModel):
    """
    Configuration for the Cassandra/Astra DB online store.
    """
    type: Literal["cassandra",
                  "feast_cassandra_online_store.cassandra_online_store.CassandraOnlineStore"] \
        = "feast_cassandra_online_store.cassandra_online_store.CassandraOnlineStore"

    # settings for connection to Cassandra / Astra DB
    hosts: Optional[List[StrictStr]] = None
    secure_bundle_path: Optional[StrictStr] = None
    port: Optional[StrictInt] = None
    keyspace: Optional[StrictStr] = None
    username: Optional[StrictStr] = None
    password: Optional[StrictStr] = None


class CassandraOnlineStore(OnlineStore):
    """
    Cassandra / Astra DB online store implementation
    """

    _cluster: Cluster = None
    _session: Session = None
    _keyspace: str = None

    def _get_session(self, config: RepoConfig):

        online_store_config = config.online_store
        if not isinstance(online_store_config, CassandraOnlineStoreConfig):
            raise CassandraInvalidConfig(E_CASSANDRA_UNEXPECTED_CONFIGURATION_CLASS)

        if self._session:
            return self._session
        if not self._session:
            # configuration consistency checks
            hosts = online_store_config.hosts
            secure_bundle_path = online_store_config.secure_bundle_path
            port = online_store_config.port or 9042
            keyspace = online_store_config.keyspace
            username = online_store_config.username
            password = online_store_config.password

            db_directions = hosts or secure_bundle_path
            if not db_directions or not keyspace:
                raise CassandraInvalidConfig(E_CASSANDRA_NOT_CONFIGURED)
            if hosts and secure_bundle_path:
                raise CassandraInvalidConfig(E_CASSANDRA_MISCONFIGURED)
            if (username is None) ^ (password is None):
                raise CassandraInvalidConfig(E_CASSANDRA_INCONSISTENT_AUTH)

            if username is not None:
                auth_provider = PlainTextAuthProvider(
                    username=username,
                    password=password,
                )
            else:
                auth_provider = None

            # creation of Cluster (Cassandra vs. Astra)
            if hosts:
                self._cluster = Cluster(
                    hosts,
                    port=port,
                    auth_provider=auth_provider,
                )
            else:
                # we use 'secure_bundle_path'
                self._cluster = cassandra.cluster.Cluster(
                    cloud={
                        'secure_connect_bundle': secure_bundle_path,
                    },
                    auth_provider=auth_provider,
                )

            # creation of Session
            self._keyspace = keyspace
            self._session = self._cluster.connect(self._keyspace)

        return self._session

    def online_write_batch(
            self,
            config: RepoConfig,
            table: FeatureView,
            data: List[
                Tuple[EntityKeyProto, Dict[str, ValueProto], datetime, Optional[datetime]]
            ],
            progress: Optional[Callable[[int], Any]],
    ) -> None:

        session = self._get_session(config)
        project = config.project
        keyspace = self._keyspace

        for entity_key, values, timestamp, created_ts in data:
            entity_key_bin = serialize_entity_key(entity_key).hex()
            timestamp = _to_naive_utc(timestamp)
            created_ts = _to_naive_utc(created_ts)
            self._write_rows(session, keyspace, project, table, entity_key_bin, values.items(), timestamp, created_ts)
            if progress:
                progress(1)

    @staticmethod
    def _fq_table_name(keyspace: str, project: str, table: FeatureView) -> str:
        return f'"{keyspace}"."{project}_{table.name}"'

    @staticmethod
    def _write_rows(session, keyspace, project, table, entity_key_bin, features_vals, timestamp, created_ts):
        fqtable = CassandraOnlineStore._fq_table_name(keyspace, project, table)
        # created_ts can be None: in that case we avoid explicitly inserting it to prevent unnecessary tombstone creation
        if created_ts is None:
            insert_cql = 'INSERT INTO {fqtable} (feature_name, value, entity_key, event_ts) VALUES (%s, %s, %s, %s);'.format(
                keyspace=keyspace,
                fqtable=fqtable,
            )
            fixed_vals = [entity_key_bin, timestamp]
        else:
            insert_cql = 'INSERT INTO {fqtable} (feature_name, value, entity_key, event_ts, created_ts) VALUES (%s, %s, %s, %s, %s);'.format(
                keyspace=keyspace,
                fqtable=fqtable,
            )
            fixed_vals = [entity_key_bin, timestamp, created_ts]
        #
        for feature_name, val in features_vals:
            session.execute(
                insert_cql,
                [feature_name, val.SerializeToString()] + fixed_vals,
            )

    def online_read(
            self,
            config: RepoConfig,
            table: FeatureView,
            entity_keys: List[EntityKeyProto],
            requested_features: Optional[List[str]] = None,
    ) -> List[Tuple[Optional[datetime], Optional[Dict[str, ValueProto]]]]:

        session = self._get_session(config)
        project = config.project
        keyspace = self._keyspace

        result: List[Tuple[Optional[datetime], Optional[Dict[str, ValueProto]]]] = []

        for entity_key in entity_keys:
            entity_key_bin = serialize_entity_key(entity_key).hex()

            feature_rows = self._read_rows_by_entity_key(session, keyspace, project,
                                                         table, entity_key_bin,
                                                         proj=['feature_name', 'value', 'event_ts'])

            res = {}
            res_ts = None
            for feature_row in feature_rows:
                # feature_name, val_bin, ts
                val = ValueProto()
                val.ParseFromString(feature_row.value)
                res[feature_row.feature_name] = val
                res_ts = feature_row.event_ts
            #
            if not res:
                result.append((None, None))
            else:
                result.append((res_ts, res))
        return result

    @staticmethod
    def _read_rows_by_entity_key(session, keyspace, project, table, entity_key_bin, proj=None):
        fqtable = CassandraOnlineStore._fq_table_name(keyspace, project, table)
        select_cql = 'SELECT {columns} FROM {fqtable} WHERE entity_key = %s;'.format(
            columns='*' if proj is None else ', '.join(proj),
            keyspace=keyspace,
            fqtable=fqtable,
        )
        return session.execute(select_cql, [entity_key_bin])

    def update(
            self,
            config: RepoConfig,
            tables_to_delete: Sequence[FeatureView],
            tables_to_keep: Sequence[FeatureView],
            entities_to_delete: Sequence[Entity],
            entities_to_keep: Sequence[Entity],
            partial: bool,
    ):

        session = self._get_session(config)
        project = config.project
        keyspace = self._keyspace

        for table in tables_to_keep:
            self._create_table(session, keyspace, project, table)
        for table in tables_to_delete:
            self._drop_table(session, keyspace, project, table)

    def teardown(
            self,
            config: RepoConfig,
            tables: Sequence[FeatureView],
            entities: Sequence[Entity],
    ):

        session = self._get_session(config)
        project = config.project
        keyspace = self._keyspace

        for table in tables:
            self._drop_table(session, keyspace, project, table)

    @staticmethod
    def _drop_table(session, keyspace, project, table):
        fqtable = CassandraOnlineStore._fq_table_name(keyspace, project, table)
        drop_cql = 'DROP TABLE IF EXISTS {fqtable};'.format(
            fqtable=fqtable,
        )
        session.execute(drop_cql)

    @staticmethod
    def _create_table(session, keyspace, project, table):
        fqtable = CassandraOnlineStore._fq_table_name(keyspace, project, table)
        create_cql = '''CREATE TABLE IF NOT EXISTS {fqtable} (
            entity_key      TEXT,
            feature_name    TEXT,
            value           BLOB,
            event_ts        TIMESTAMP,
            created_ts      TIMESTAMP,
            PRIMARY KEY ((entity_key), feature_name)
        ) WITH CLUSTERING ORDER BY (feature_name ASC);'''.format(
            fqtable=fqtable,
        )
        session.execute(create_cql)

def _to_naive_utc(ts: datetime):
    return ts
    # if ts.tzinfo is None:
    #     return ts
    # else:
    #     return ts.astimezone(pytz.utc).replace(tzinfo=None)


