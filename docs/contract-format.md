# Intract Contract Format

An Intract contract is a one-line, self-describing validation contract.

```text
@intract.v1 scope:<scope> intent:<action>:<object> priority:<1-5> domain:<domain> input:<inputs> output:<outputs> effect:<effects> forbid:<effects> require:<subintents> validate:<rules> meaning:"plain explanation"
```

Example (comment or decorator — both parse identically):

```python
# @intract.v1 scope:function intent:validate:user_permission priority:1 domain:security input:user,resource output:allowed effect:none forbid:write,network require:none validate:input_presence,return_value,no_forbidden_effect meaning:"check if user may modify resource without changing state"
```

```rust
@intract.v1 uri="intract://src/decoder.rs?func=decode_header#id=safe-decoder&forbid=unsafe"
```
