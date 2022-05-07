# TODO

## Code improvements

Use `@tracing_span` and `@log_exception_and_usage`

Try to map to Feast errors (`feast/errors.py`)

Test Astra DB

Better handling of `feast_test.py` and secrets

refactor/regroup CQL layer

batch insertion within each `entity_key`

use prepared statements for reads and writes, cache them manually and per-table

add type annotations in all function signatures

(to what extent?) sanitize table names

ignored params to `online_read`: `requested_features`. Implement its usage

more settings in connection creation (CL, LBP, ... ?) perhaps later

## Open questions

we avoid insertion of nulls for `created_ts`: check it does not create problems (potentially, a wrong ts from a preexisting row?)

check if to_naive_utc is a feast requirement somehow (so far commented to identity)

ignored params to `update`: `['entities_to_delete, entities_to_keep, partial]`. Not sure what they should control, docs says little to nothing. Make this clear (majos online stores seem to ignore these params as well)

ignored param `entities` to `teardown`: this is also ignored by major stores, check better

## Missing components

setup.py / package distribution stuff

is a provider needed?

Write a README and basic doc
