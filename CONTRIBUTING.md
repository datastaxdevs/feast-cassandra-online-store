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

- create an empty virtualenv, such as `feast-cassandra-39` ;
- run `pip install --upgrade pip` ;
- run `pip install feast` ;
- run `python setup.py install` .