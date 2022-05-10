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
[Awesome Astra](#)
documentation.

## Features

The plugin leverages the architecture of Cassandra for optimal performance:

- table partitioning tailored to data access pattern;
- prepared statements.

## Development quick guide

### Dev environment

_Instructions to develop this package:_

Once cloned, make sure the `feast` Git [submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) is cloned as well:
in root of repo, `git submodule init` and `git submodule update`.
(To advance the commit of the submodule if necessary, `git submodule update --remote` .)
(If advancing `feast` submodule, one may have to rebuild the protobuf assets:
`pip install --upgrade setuptools` and `make protos` in the `feast` subdir.)

Create a fresh development virtualenv, e.g. `feast-cassandra-dev-39`, and
`pip install --upgrade pip` in it.

Go to the repo's root. Add this path to the python path, e.g. creating a text
file such as `~/.virtualenvs/feast-cassandra-dev-39/lib/python3.9/site-packages/custom-path.pth`
with the path in it. Then deactivate and activate the virtualenv again.
_This steps is needed only to make the universal unit test able to import the test
config definitions later._

Install `pip install -r requirements-dev.txt` .

Install this plugin in develop mode: `python setup.py develop` .

Also install `feast` itself in the same way: `cd feast; pip install -e ".[dev]"; cd ..` .

Now unit tests can be run: `cd feast; make test-python; cd ..` .

But, most important, integration tests can be run:

- copy `plugin_tests/.env.sample` to `plugin_tests.env` and adjust its settings;
- run either `export FULL_REPO_CONFIGS_MODULE='plugin_tests.cassandra_tests'` or `export FULL_REPO_CONFIGS_MODULE='plugin_tests.astra_db_tests'` ;
- finally run `cd feast; make test-python-universal; cd ..` (and expect at most one single failure about GCP credentials not found).

### Installed (from local) package

_An environment with "actual" installations, needed for example to run the
"Quick usage" setups given above, is obtained as follows:_

Create an empty virtualenv, such as `feast-cassandra-39`.

Run `pip install --upgrade pip`.

Run `pip install feast`

Run `python setup.py install`.

Done.

