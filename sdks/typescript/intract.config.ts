import { inlineContract } from "./src/index";

export default {
  manifest: "intract.yaml",
  plugins: ["inline", "manifest", "openapi", "docker", "github_actions"],
  failOn: ["violation", "invalid_manifest", "missing_required_p1"],
  helpers: { inlineContract }
};
