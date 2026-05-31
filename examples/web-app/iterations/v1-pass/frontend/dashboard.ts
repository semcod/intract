// @intract.v1 scope:function intent:ui:render_dashboard priority:3 domain:frontend input:profile output:view effect:read forbid:network validate:return_value,no_forbidden_effect meaning:"Render dashboard view model from profile data passed from backend"
export function renderDashboard(profile: { name: string; role?: string }) {
  return {
    title: `Welcome, ${profile.name}`,
    widgets: ["recent-activity", "permissions"],
    mode: "mock-v1",
  };
}
