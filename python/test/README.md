# Property based testing

Typically when writing unit tests, the code author comes up with examples, and asserts behavior about their code,
specific to those examples. Property based tests offer an alternative approach. Instead, the test framework randomly
generates test cases, and the author asserts properties that must be true for all test cases.

We use [hypothesis](https://hypothesis.readthedocs.io/en/v1.8.4/quickstart.html) to do property based testing in our
Python codebase. Their docs are a good starting point to learn about this testing approach.
