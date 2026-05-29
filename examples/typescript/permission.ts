// @intract.v1 scope:function intent:validate:user_permission priority:1 domain:security input:user,resource output:allowed effect:none forbid:network,write require:none validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"check if user can modify resource without network or writes"
function canUpdateResource(user: User, resource: Resource): boolean {
  const allowed = user.isAdmin || resource.ownerId === user.id;
  return allowed;
}
