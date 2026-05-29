# @intract.v1 scope:function intent:parse:extensions priority:2 domain:cli input:raw_extensions output:extension_list effect:none forbid:network,write require:none validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"parse raw extension string into normalized extension list"
def parse_extensions(raw_extensions: str) -> list[str]:
    extension_list = [
        item.strip().lower()
        for item in raw_extensions.split(",")
        if item.strip()
    ]
    return extension_list
