from intract.parser import parse_contract_line


def test_parse_full_contract_line():
    line = (
        '# @intract.v1 scope:function intent:validate:user_permission priority:1 '
        'domain:security input:user,resource output:allowed effect:none '
        'forbid:write,network validate:input_presence,return_value '
        'meaning:"check permission"'
    )
    contract = parse_contract_line(line)

    assert contract is not None
    assert contract.action == "validate"
    assert contract.object == "user_permission"
    assert contract.priority == 1
    assert contract.scope == "function"
    assert contract.domain == "security"
    assert contract.inputs == ("user", "resource")
    assert contract.outputs == ("allowed",)
    assert contract.forbidden == ("write", "network")


def test_parse_comment_prefix_ts():
    line = "// @intract.v1 scope:function intent:parse:extensions priority:2"
    contract = parse_contract_line(line)
    assert contract is not None
    assert contract.action == "parse"
    assert contract.object == "extensions"


def test_parse_malformed_quoted_contract_returns_none():
    line = '# @intract.v1 scope:function intent:parse:broken meaning:"unterminated'

    assert parse_contract_line(line) is None
