# @intract.v1 scope:function intent:scan:project_files priority:1 domain:scanner input:ScanConfig output:file_list effect:read forbid:network validate:no_forbidden_effect
def scan_project_files(config):
    root = config.get("root", ".")
    return [f"{root}/src/scanner.py", f"{root}/src/parser_a.py", f"{root}/src/parser_b.py"]
