const vscode = require("vscode");

function runIntract(args) {
  const config = vscode.workspace.getConfiguration("intract");
  const python = config.get("pythonPath", "python");
  const terminal = vscode.window.createTerminal({ name: "Intract" });
  terminal.show();
  terminal.sendText(`${python} -m intract ${args.join(" ")}`);
}

function runShell(command) {
  const terminal = vscode.window.createTerminal({ name: "Intract" });
  terminal.show();
  terminal.sendText(command);
}

function workspaceRoot() {
  return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || ".";
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand("intract.validateProject", () => {
      const folder = workspaceRoot();
      const manifest = vscode.workspace.getConfiguration("intract").get("manifest", "intract.yaml");
      runIntract(["validate", folder, "--manifest", manifest]);
    }),
    vscode.commands.registerCommand("intract.checkStaged", () => {
      const folder = workspaceRoot();
      runIntract(["check", folder, "--staged", "--hunks"]);
    }),
    vscode.commands.registerCommand("intract.webAppDemo", () => {
      const root = workspaceRoot();
      runShell(`bash ${root}/examples/web-app/run-demo.sh`);
    }),
    vscode.commands.registerCommand("intract.webAppMock", async () => {
      const root = workspaceRoot();
      runShell(`bash ${root}/examples/web-app/run-demo.sh`);
      const uri = vscode.Uri.parse("http://localhost:8765/mock/index.html");
      runShell(`python -m http.server 8765 --directory ${root}/examples/web-app`);
      await vscode.env.openExternal(uri);
      vscode.window.showInformationMessage(
        "Web App Mock: http://localhost:8765/mock/index.html (Ctrl+Click if browser did not open)"
      );
    })
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
