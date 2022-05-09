# TODO

## Code improvements

### For release

use prepared statements for reads and writes, cache them manually and per-table
and log the caching and the preparing

batch insertion within each `entity_key`
on a single partition can be UNLOGGED

### Later

The usual protocol version and load balancer warnings, see if want to go away through settings?
(both Astra and Cassandra)

(to what extent?) sanitize table names

more settings in connection creation (CL, LBP, ... ?) perhaps later

## Open questions

we avoid insertion of nulls for `created_ts`: check it does not create problems (potentially, a wrong ts from a preexisting row?)

ignored params to `update`: `['entities_to_delete, entities_to_keep, partial]`. Not sure what they should control, docs says little to nothing. Make this clear (major online stores seem to ignore these params as well)

ignored param `entities` to `teardown`: this is also ignored by major stores, check better

is it necessary to create a provider? (it seems it does not add much)

my usage of with `tracing_span`: individually for each call to the CQL driver ops, is that the right way? (comparing with other datastores one is not so sure)

## Missing components

setup.py / package distribution stuff
    REQUIRES_PYTHON = ">=3.7.0"
    python_requires=REQUIRES_PYTHON,

is a provider needed?

Write a README and basic doc
