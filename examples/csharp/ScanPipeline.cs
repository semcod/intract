// @intract.v1 scope:file intent:implement:scan_pipeline priority:1 domain:analysis input:sourceTree output:duplicationMap effect:read forbid:network require:scan.project_files,extract.code_blocks,detect.duplicates,render.report validate:required_intents,no_forbidden_effect meaning:"file should implement scan pipeline from files to duplication report"

// @intract.v1 scope:function intent:scan:project_files priority:1 domain:scanner input:sourceTree output:fileList effect:read forbid:network validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"collect source files from project tree"
public List<string> CollectFiles(string sourceTree) {
    var fileList = Directory.GetFiles(sourceTree, "*.cs").ToList();
    return fileList;
}
