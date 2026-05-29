# Validation Model

Supported validation rules:

| Rule | Meaning |
|---|---|
| `input_presence` | Required inputs appear in the source. |
| `output_presence` | Required outputs appear in the source. |
| `return_value` | The code appears to return/yield a value. |
| `no_forbidden_effect` | Forbidden effects such as `network` or `write` are not detected. |
| `effect_match` | Observed effects match declared effects. |
| `required_intents` | Required sub-intents are present in the project. |
