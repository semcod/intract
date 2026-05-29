import { inlineContract } from "../src/index";

console.log(inlineContract({
  scope: "function",
  intent: "validate:user_permission",
  priority: 1,
  domain: "security",
  input: ["user", "resource"],
  output: ["allowed"],
  forbid: ["network", "write"],
  validate: ["input_presence", "return_value", "no_forbidden_effect"],
  meaning: "check whether user can modify resource without changing state"
}));
