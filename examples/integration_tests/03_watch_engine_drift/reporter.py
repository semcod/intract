# @intract.v1 scope:function intent:render:summary_report priority:3 domain:reporting input:file_list output:summary effect:none forbid:network,write require:none validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"render summary report from file list without side effects"
def render_summary(file_list: list[str]) -> str:
    summary = f"Files: {len(file_list)}"
    return summary
