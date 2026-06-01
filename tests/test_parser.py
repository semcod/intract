from intract.parser import parse_contract_line


DECODER_URI = (
    'intract://src/decoder.rs?func=decode_header#id=safe-decoder&forbid=unsafe'
)


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


def test_parse_decorator_matches_comment_intent_form():
    comment = "// @intract.v1 scope:function intent:decode:raw forbid:unsafe"
    decorator = "@intract.v1 scope:function intent:decode:raw forbid:unsafe"
    from_comment = parse_contract_line(comment)
    from_decorator = parse_contract_line(decorator)

    assert from_comment is not None
    assert from_decorator is not None
    assert from_comment.action == from_decorator.action == "decode"
    assert from_comment.object == from_decorator.object == "raw"
    assert from_comment.forbidden == from_decorator.forbidden == ("unsafe",)


def test_parse_uri_decorator_matches_comment_form():
    comment = f'// @intract.v1 uri="{DECODER_URI}"'
    decorator = f'@intract.v1 uri="{DECODER_URI}"'
    from_comment = parse_contract_line(comment)
    from_decorator = parse_contract_line(decorator)

    assert from_comment is not None
    assert from_decorator is not None
    assert from_comment.contract_id == from_decorator.contract_id == "safe-decoder"
    assert from_comment.forbidden == from_decorator.forbidden == ("unsafe",)
    assert from_comment.action == from_decorator.action == "safe"
    assert from_comment.object == from_decorator.object == "decoder"


def test_parse_rust_attribute_wrapper():
    line = f'#[intract.v1 uri="{DECODER_URI}"]'
    contract = parse_contract_line(line)

    assert contract is not None
    assert contract.contract_id == "safe-decoder"
    assert contract.forbidden == ("unsafe",)
