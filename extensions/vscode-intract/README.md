# Intract VS Code Extension

Highlight `@intract.v1` tags and run the Intract CLI from the editor.

## Install from VSIX (local)

```bash
cd extensions/vscode-intract
npm install -g @vscode/vsce
vsce package --no-dependencies
code --install-extension intract-intent-contracts-0.1.0.vsix
```

## Publish to Visual Studio Marketplace

1. Create a publisher at https://marketplace.visualstudio.com/manage
2. Generate a Personal Access Token with **Marketplace → Manage**
3. Add repository secret `VSCE_PAT`
4. Tag and push: `git tag vscode-v0.1.0 && git push origin vscode-v0.1.0`
5. Workflow `.github/workflows/vscode-extension.yml` packages and publishes the VSIX

Manual publish:

```bash
vsce login semcod
vsce publish --no-dependencies
```

## Features

- Syntax injection for `@intract.v1` in Python, TypeScript, JavaScript, C#, Java, Go, Rust
- Commands: **Intract: Validate Project**, **Intract: Check Staged (Hunks)**

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `intract.manifest` | `intract.yaml` | Manifest path |
| `intract.pythonPath` | `python` | Python executable for CLI |
