# Intract VS Code Extension

Minimal extension for `@intract.v1` comment highlighting and CLI tasks.

## Install locally

```bash
cd extensions/vscode-intract
code --install-extension .
```

Or symlink into your VS Code extensions directory.

## Features

- Syntax injection for `@intract.v1` tags in Python, TypeScript, JavaScript and C#
- Commands:
  - **Intract: Validate Project**
  - **Intract: Check Staged (Hunks)**

## Settings

- `intract.manifest` — default manifest path (`intract.yaml`)
