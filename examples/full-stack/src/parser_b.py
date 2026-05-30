# @intract.v1 scope:function intent:read:extension_list priority:2 domain:cli input:value output:list effect:none forbid:network validate:return_value
def load_extension_list(value):
    return value.split(",")
