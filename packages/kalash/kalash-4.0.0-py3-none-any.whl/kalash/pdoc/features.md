# Features

## What **you** can do with Kalash

- Run Software or Hardware tests in an automated context as well as locally:
    - As singular Python Scripts
    - As test suites defined in a simple declarative [YAML](#yaml-config-file-specification) file or more flexible [Python configuration files](#python-config-file-specification)
    - In [isolation](#why-use-kalash) from lower-level automation server job configuration (e.g. you don't need to manage Jenkins to change the definition of a test suite to be triggered by a job)
- [Filter](#yaml-config-file-specification) test cases by way more than just a name, defining rich, complex test suites
- Document metadata for your test cases in a manner that is [both human-readable and machine-readable](#creating-test-cases)
- Generate [standard XML XUnit reports](#reports)
- Log whatever happens within the test cases on a [per-test-case level of granularity](#logging)
- [Parameterize](#accessing-configuration-from-within-test-cases) test cases easily
- Perform [hypothetical runs](#hypothetical-runs)

Read [Why Use Kalash](#why-use-kalash) to get a more comprehenisve overview of the system.

## Notable Features Available

- [Filtering](#yaml-config-file-specification) by metadata tags
- [Python](#python-config-file-specification) or [YAML](#yaml-config-file-specification) declarative-style configuration files for test suites
- [Setup and Teardown](#setup-and-teardown) scripts are supported
- `--no-recurse` option
- `--fail-fast` option
- Each test case has its own [logger](#logging)
- `--what-if` option
- [Logger configuration](#logging) via CLI
- [Dynamic parametrization](#accessing-configuration-from-within-test-cases) of the test cases

## Notable Features Planned

- Log files grouping based on arbitrary metadata tags
- Stable last-result filtering
- JIRA integration - loading metadata automatically from JIRA tickets
