# @intract.v1 scope:function intent:detect:duplicates priority:1 domain:analysis input:blocks output:groups effect:read forbid:network validate:return_value
def detect_duplicates(blocks):
    return [{"id": "dup_001", "count": len(blocks)}]
