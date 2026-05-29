# Intract Plugins and SDKs

Intract supports plugin types:

- `ParserPlugin` — extracts contracts from artifacts.
- `ValidatorPlugin` — validates contracts against artifacts.
- `ReporterPlugin` — renders reports.
- `IntegrationPlugin` — installs project integrations such as pre-commit, GitHub Actions, CI.

Python plugins are loaded through entry points:

```toml
[project.entry-points."intract.parsers"]
my_parser = "my_package:MyParser"

[project.entry-points."intract.validators"]
my_validator = "my_package:MyValidator"

[project.entry-points."intract.reporters"]
my_reporter = "my_package:MyReporter"
```

External SDKs can produce the same contract fields in their native ecosystem.
