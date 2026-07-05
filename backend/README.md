# Slide Merger Backend

> Python backend of Slide Merger

We assume you are in the `backend` subdirectory when running commands.

## Install

### libgdiplus

**Windows** :

Nothing to do, already packaged in the system.

**Ubuntu** :

```bash
sudo apt-get install libgdiplus
```

**MacOS** :

```bash
brew install mono-libgdiplus
```

### .Net runtime

**Ubuntu** :

```bash
sudo apt-get install aspnetcore-runtime-8.0
```

**Other systems** :

Install form [Microsoft.com](https://dotnet.microsoft.com/download/dotnet/8.0).

### Python environment

This project use [uv](https://docs.astral.sh/uv/),
an extremely fast Python package and project manager, written in Rust.

```bash
uv sync
```

## [Activate environment](https://docs.astral.sh/uv/pip/environments/#using-a-virtual-environment)

Useful to run `task` commands

**macOS/Linux** :

```bash
source .venv/bin/activate
```

**windows** :

```bash
.venv\Scripts\activate
```

## Configure

**TODO** Configuration net set yet

## Run

**TODO** Main file not done yet

## Tests

**macOS/Linux** :

```bash
task test
```

**windows** :

```bash
task test-windows
```
