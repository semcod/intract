import requests

# @intract.v1 scope:function intent:auth:check_permission priority:1 domain:security input:user,resource output:allowed effect:read forbid:network,write validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"Check permission locally without network or writes"
def check_permission(user, resource) -> bool:
    response = requests.get(f"https://auth.example/allow/{user['id']}/{resource['id']}")
    return response.status_code == 200
