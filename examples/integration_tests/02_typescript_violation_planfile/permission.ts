// @intract.v1 scope:function intent:validate:user_permission priority:1 domain:security input:user,resource output:allowed effect:none forbid:network,write require:none validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"check if user can modify resource without network or writes"
async function canUpdateResource(user: User, resource: Resource): Promise<boolean> {
  const response = await fetch(`/api/permissions/${user.id}/${resource.id}`);
  const allowed = await response.json();
  return allowed;
}
