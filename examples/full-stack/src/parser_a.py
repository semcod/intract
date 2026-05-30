# @intract.v1 scope:function intent:parse:extensions priority:2 domain:cli input:raw output:list effect:none forbid:network validate:input_presence,return_value
def parse_extensions(raw):
    return [item.strip() for item in raw.split(",") if item.strip()]
