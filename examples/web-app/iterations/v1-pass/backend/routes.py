# @intract.v1 scope:function intent:api:read_profile priority:2 domain:api input:user_id output:profile effect:read forbid:network validate:return_value,no_forbidden_effect meaning:"Build profile payload from in-memory user store"
def read_profile(user_id: str, users: dict) -> dict:
    profile = users.get(user_id, {"id": user_id, "name": "Guest"})
    return {"profile": profile, "source": "local-store"}
