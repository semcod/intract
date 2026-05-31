# @intract.v1 scope:function intent:auth:check_permission priority:1 domain:security input:user,resource output:allowed effect:read forbid:network,write validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"Check permission locally without network or writes"
def check_permission(user, resource) -> bool:
    if user.get("role") == "admin":
        return True
    return resource.get("owner_id") == user.get("id")
