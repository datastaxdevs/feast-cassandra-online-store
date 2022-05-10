# Feast Cassandra / Astra DB online store plugin

A [Feast](https://feast.dev/)
plugin to use
[Apache Cassandra™](https://cassandra.apache.org) / 
[Astra DB](https://astra.datastax.com/) as online store.

## Installation

Install the plugin alongside Feast with:

```
pip install feast-cassandra
```

## Quick usage

Once the package is installed, switching online store to Cassandra / Astra DB
is a matter of altering the `online_store` key in `feature_store.yaml`.

With reference to the [Feast quickstart](https://docs.feast.dev/getting-started/quickstart),
the minimal steps are:

1. (assuming both `feast` and this plugin are installed)
2. creating a feature repository, `feast init feature_repo`;
3. `cd feature_repo`;
4. editing the `feature_store.yaml` as detailed below;
5. all subsequent steps proceed as usual.

### Cassandra setup

The only required settings are `hosts` and `type`. The port number
is to be provided only if different than the default (9042),
and username/password only if the database requires authentication.

```yaml
[...]
online_store:
    type: feast_cassandra_online_store.cassandra_online_store.CassandraOnlineStore
    hosts:
        - 192.168.1.1
        - 192.168.1.2
        - 192.168.1.3
    keyspace: KeyspaceName
    port: 9042        # optional
    username: user    # optional
    password: secret  # optional
```

### Astra DB setup:

To point Feast to using an Astra DB instance as online store, an 
[Astra DB token](https://awesome-astra.github.io/docs/pages/astra/create-token/#c-procedure)
with "Database Administrator" role is required: provide the Client ID and
Client Secret in the token as username and password.

The 
["secure connect bundle"](https://awesome-astra.github.io/docs/pages/astra/download-scb/#c-procedure)
for connecting to the database is also needed:
its full path must be given in the configuration below:

```yaml
[...]
online_store:
    type: feast_cassandra_online_store.cassandra_online_store.CassandraOnlineStore
    secure_bundle_path: /path/to/secure/bundle.zip
    keyspace: KeyspaceName
    username: Client_ID
    password: Client_Secret
```

### More info

For a more detailed walkthrough, please see the
[Awesome Astra](https://awesome-astra.github.io/docs/pages/tools/)
documentation.

## Features

The plugin leverages the architecture of Cassandra for optimal performance:

- table partitioning tailored to data access pattern;
- prepared statements.
