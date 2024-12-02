# Univariate Statistical Analysis of a Non-Canonical Genre

This repository contains the development environment and code for the paper _“Univariate Statistical Analysis of a Non-Canonical Genre”_.  
The environment is managed with [Nix](https://nixos.org/) to ensure reproducibility.

## Overview

This project leverages Nix to define a reproducible development environment.
The following use cases are supported:

1. **Replicating Results**: Build the project to execute the Jupyter notebook and retrieve the analysis results.
2. **Development and Further Analysis**: Modify the source code or perform additional experiments.

## Usage with Nix ❄️

### Building the Project

To build the project and execute the Jupyter notebook, run:

```sh
$ nix build
```

The results will be stored in the Nix store and accessible via the `result` symlink.

Alternatively, you can build the project directly from GitHub without cloning the repository:

```sh
$ nix build github:v-ji/einakter-chr2024-stats
```

### Development Environment

To enter the development environment with all required dependencies, run:

```sh
$ nix develop
```

Once inside, start the Jupyter Notebook with:

```sh
$ jupyter notebook main.ipynb
```

## Usage with Docker 🐳

For users who do not have Nix installed, a `x86_64-linux` Docker image is available.  
Follow these steps to use the Docker image:

### Loading the Docker Image

Download the image from the Releases section and load it:

```sh
$ docker image load < einakter-chr2024-notebook-env-1.0.0-x86_64-linux.tar.gz
$ docker run -it --rm -p 8888:8888 --platform linux/amd64 einakter-chr2024-notebook-env:1.0.0
```

> [!NOTE]
> This Docker image is built entirely using Nix and includes only minimal dependencies.  
> The `flake.nix` file contains the image definition under the `dockerShell` attribute.

### Building Inside the Container

Once the container is running, build the project using:

```sh
$ buildDerivation
```

The outputs (results) will be available in the `$out` directory.

### Development Inside the Container

To modify the source code or conduct additional analysis, obtain a writeable copy of the source directory. This is automatically available if you run `buildDerivation`. Alternatively, to copy the source without building, execute:

```sh
$ unpackPhase
```

Afterward, start the Jupyter Notebook:

```sh
$ jupyter notebook *-source/ --no-browser --ip=0.0.0.0
```

Access the notebook in your browser at `http://localhost:8888`.

## Requirements for Non-Nix Users

A `requirements.txt` file is provided as a best-effort alternative for non-Nix users.  
However, **using Nix is strongly recommended** for full reproducibility.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
