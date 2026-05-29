# @intract.v1 scope:function intent:scan:project_files priority:1 domain:scanner input:source_tree output:file_list effect:read forbid:network,write require:none validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"collect Python files from project tree without network or writes"
def collect_project_files(source_tree: str) -> list[str]:
    file_list = [
        path
        for path in source_tree.splitlines()
        if path.endswith(".py")
    ]
    return file_list
