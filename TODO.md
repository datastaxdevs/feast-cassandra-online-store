# TODO

## Improvements

#### Issues

Issue template(s) on github. (not if planning to enter Feast' repo itself).



## Open questions/issues

#### Schema changes?

"create table if not exist", what about a table changes its schema?

#### No-insertion cells

We currently avoid altogether insertion of nulls for `created_ts` when missing:
check it does not create problems (potentially, a wrong ts from a preexisting row?)

#### Ignored parameters in store methods

There are ignored params to `update`: `[entities_to_delete, entities_to_keep, partial]`.
Not sure what they should control, docs says little to nothing.

Same for param `entities` to `teardown`: this is also ignored by major stores.

Make sure this is OK.

#### Provider?

Is it necessary to create a provider? (it seems it does not add much in this case)

#### Tracing span

Usage of `with tracing_span(...)` here:
individually for each call to the CQL driver ops.

Is that the right way? (comparing with other datastores one is not so sure)
