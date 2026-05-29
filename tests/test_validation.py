from intract.parser import extract_contract_records_from_text
from intract.signature import build_signature
from intract.validation import validate_contract_against_source
from intract.models import ValidationStatus


def test_python_contract_passes():
    source = (
        '# @intract.v1 scope:function intent:parse:extensions priority:2 domain:cli '
        'input:raw_extensions output:extension_list effect:none forbid:network,write '
        'validate:input_presence,output_presence,return_value,no_forbidden_effect '
        'meaning:"parse raw extension string into normalized extension list"\n'
        'def parse_extensions(raw_extensions: str) -> list[str]:\n'
        '    extension_list = [item.strip().lower() for item in raw_extensions.split(",") if item.strip()]\n'
        '    return extension_list\n'
    )
    record = extract_contract_records_from_text(source, file_path="sample.py")[0]
    signature = build_signature(record)
    result = validate_contract_against_source(signature, source)
    assert result.status == ValidationStatus.PASS


def test_typescript_contract_detects_network_violation():
    source = (
        '// @intract.v1 scope:function intent:validate:user_permission priority:1 domain:security '
        'input:user,resource output:allowed effect:none forbid:network,write '
        'validate:input_presence,output_presence,return_value,no_forbidden_effect '
        'meaning:"check permission without network"\n'
        'async function canUpdateResource(user: User, resource: Resource): Promise<boolean> {\n'
        '  const response = await fetch(`/api/permissions/${user.id}/${resource.id}`);\n'
        '  const allowed = await response.json();\n'
        '  return allowed;\n'
        '}\n'
    )
    record = extract_contract_records_from_text(source, file_path="permission.ts")[0]
    signature = build_signature(record)
    result = validate_contract_against_source(signature, source)
    assert result.status == ValidationStatus.VIOLATION
    assert result.violations
