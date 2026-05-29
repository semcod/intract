# Quick enable Intract in a new project

## Python

```bash
pip install intract
intract init .
```

Add to `pyproject.toml`:

```toml
[tool.intract]
manifest = "intract.yaml"
mode = "changed"
fail_on = ["violation", "invalid_manifest"]
```

## Node / TypeScript

```bash
npm install -D @intract/sdk
```

Add to `package.json`:

```json
{
  "scripts": {
    "intract": "intract validate . --manifest intract.yaml"
  }
}
```

## Go

```bash
go get github.com/intract/sdk-go
```

## Rust

```toml
[dependencies]
intract-sdk = "0.1"
```

## Java

```gradle
dependencies {
    implementation "io.intract:intract-sdk:0.1.0"
}
```

## C#

```bash
dotnet add package Intract.Sdk
```
