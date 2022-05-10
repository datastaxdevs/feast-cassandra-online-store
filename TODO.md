# TODO

## Improvements

#### Documentation

link to the right Awesome Astra page in the README.

#### More settings

Add `protocol_version` and possibly `local_dc`/`load_balancing_policy`, to the settings
for faster startup, futureproof usage of drivers and less clutter in the logs.

As the config is given through a yaml, some rework is needed when instantiating the `Cluster`.

#### Sanitize table names

Make sure no accidental syntax-breaking naming gets in the way.

#### Issues

Issue template(s) on github.


## Open questions/issues

#### No-insertion cells

We currently avoid altogether insertion of nulls for `created_ts` when missing:
check it does not create problems (potentially, a wrong ts from a preexisting row?)

#### Ignored parameters in store methods

Ther are ignored params to `update`: `['entities_to_delete, entities_to_keep, partial]`.
Not sure what they should control, docs says little to nothing.

Same for param `entities` to `teardown`: this is also ignored by major stores.

Make sure this is OK.

#### Provider?

Is it necessary to create a provider? (it seems it does not add much in this case)

#### Tracing span

Usage of `with tracing_span(...)` here:
individually for each call to the CQL driver ops.

Is that the right way? (comparing with other datastores one is not so sure)
