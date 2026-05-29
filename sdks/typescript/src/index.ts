export type IntractContract = {
  scope: string;
  intent: string;
  priority?: number;
  domain?: string;
  input?: string[];
  output?: string[];
  effect?: string[];
  forbid?: string[];
  require?: string[];
  validate?: string[];
  meaning?: string;
};

function csv(values?: string[]): string | undefined {
  if (!values || values.length === 0) return undefined;
  return values.join(",");
}

export function inlineContract(contract: IntractContract, prefix = "//"): string {
  const parts = [
    "@intract.v1",
    `scope:${contract.scope}`,
    `intent:${contract.intent}`,
    `priority:${contract.priority ?? 3}`
  ];

  if (contract.domain) parts.push(`domain:${contract.domain}`);
  if (csv(contract.input)) parts.push(`input:${csv(contract.input)}`);
  if (csv(contract.output)) parts.push(`output:${csv(contract.output)}`);
  if (csv(contract.effect)) parts.push(`effect:${csv(contract.effect)}`);
  if (csv(contract.forbid)) parts.push(`forbid:${csv(contract.forbid)}`);
  if (csv(contract.require)) parts.push(`require:${csv(contract.require)}`);
  if (csv(contract.validate)) parts.push(`validate:${csv(contract.validate)}`);
  if (contract.meaning) parts.push(`meaning:"${contract.meaning}"`);

  return `${prefix} ${parts.join(" ")}`;
}

export function manifestContract(contract: IntractContract): Record<string, unknown> {
  return contract;
}
