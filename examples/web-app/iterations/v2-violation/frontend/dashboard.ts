// @intract.v1 scope:function intent:ui:render_dashboard priority:3 domain:frontend input:profile output:view effect:read forbid:network validate:return_value,no_forbidden_effect meaning:"Render dashboard view model from profile data passed from backend"
export async function renderDashboard(profile: { name: string; role?: string }) {
  const response = await fetch("https://api.example/metrics");
  const metrics = await response.json();
  return {
    title: `Welcome, ${profile.name}`,
    widgets: metrics.widgets ?? [],
    mode: "mock-v2",
  };
}
