namespace Intract.Sdk;

public sealed class IntractContract
{
    public string Scope { get; init; } = "function";
    public string Intent { get; init; } = "";
    public int Priority { get; init; } = 3;
    public string Domain { get; init; } = "";
    public string[] Input { get; init; } = [];
    public string[] Output { get; init; } = [];
    public string[] Effect { get; init; } = [];
    public string[] Forbid { get; init; } = [];
    public string[] Require { get; init; } = [];
    public string[] Validate { get; init; } = [];
    public string Meaning { get; init; } = "";

    public string Inline(string prefix = "//")
    {
        var parts = new List<string>
        {
            "@intract.v1",
            $"scope:{Scope}",
            $"intent:{Intent}",
            $"priority:{Priority}"
        };

        if (!string.IsNullOrWhiteSpace(Domain)) parts.Add($"domain:{Domain}");
        if (Input.Length > 0) parts.Add($"input:{string.Join(",", Input)}");
        if (Output.Length > 0) parts.Add($"output:{string.Join(",", Output)}");
        if (Effect.Length > 0) parts.Add($"effect:{string.Join(",", Effect)}");
        if (Forbid.Length > 0) parts.Add($"forbid:{string.Join(",", Forbid)}");
        if (Require.Length > 0) parts.Add($"require:{string.Join(",", Require)}");
        if (Validate.Length > 0) parts.Add($"validate:{string.Join(",", Validate)}");
        if (!string.IsNullOrWhiteSpace(Meaning)) parts.Add($"meaning:\"{Meaning}\"");

        return $"{prefix} {string.Join(" ", parts)}";
    }
}
