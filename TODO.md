# TODO

## Testing

test (c* and astra) in a real case now and at the end of improvements

## Code improvements

The usual protocol version and load balancer warnings, see if want to go away through settings?
(both Astra and Cassandra)

Use `@tracing_span` and `@log_exception_and_usage`

Try to map to Feast errors (`feast/errors.py`)

refactor/regroup CQL layer

batch insertion within each `entity_key`

use prepared statements for reads and writes, cache them manually and per-table

add type annotations in all function signatures

(to what extent?) sanitize table names

ignored params to `online_read`: `requested_features`. Implement its usage

more settings in connection creation (CL, LBP, ... ?) perhaps later

docstrings as education requires

## Open questions

we avoid insertion of nulls for `created_ts`: check it does not create problems (potentially, a wrong ts from a preexisting row?)

check if to_naive_utc is a feast requirement somehow (so far commented to identity)

ignored params to `update`: `['entities_to_delete, entities_to_keep, partial]`. Not sure what they should control, docs says little to nothing. Make this clear (major online stores seem to ignore these params as well)

ignored param `entities` to `teardown`: this is also ignored by major stores, check better

is it necessary to create a provider? (it seems it does not add much)

## Missing components

setup.py / package distribution stuff

is a provider needed?

Write a README and basic doc
