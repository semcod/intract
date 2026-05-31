const vscode = require("vscode");

function runIntract(args) {
  const config = vscode.workspace.getConfiguration("intract");
  const python = config.get("pythonPath", "python");
  const terminal = vscode.window.createTerminal({ name: "Intract" });
  terminal.show();
  terminal.sendText(`${python} -m intract ${args.join(" ")}`);
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand("intract.validateProject", () => {
      const folder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || ".";
      const manifest = vscode.workspace.getConfiguration("intract").get("manifest", "intract.yaml");
      runIntract(["validate", folder, "--manifest", manifest]);
    }),
    vscode.commands.registerCommand("intract.checkStaged", () => {
      const folder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || ".";
      runIntract(["check", folder, "--staged", "--hunks"]);
    })
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
