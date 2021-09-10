
# Transform

This service is responsible for doing data transformations. A transformation is
defined as an operation that does not alter the form of the data, but its
substantial content. This might for example be a lag operation, where values
are propagated spatially or temporally.

All transform operations must return data at the same LOA as the input.

For resolving the base data, Transform asks the query manager responsible for
routing to data, which also routs to Transform. This means that transformations
can be composed.
For information about how to contribute, see [contributing](https://www.github.com/prio-data/contributing).
