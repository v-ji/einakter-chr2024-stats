# Univariate Statistical Analysis of a Non-Canonical Genre

This repository contains the development environment and code for the paper “Univariate Statistical Analysis of a Non-Canonical Genre”.
The environment is managed using Nix to ensure reproducibility.

## Reproducibility with Nix

This project uses [Nix](https://nixos.org/) to manage dependencies and ensure a reproducible environment.
The `flake.nix` file defines the development environment, including the necessary Python packages and datasets.

### Key Components

- **`flake.nix`**: Defines the development environment and dependencies.
- **`flake.lock`**: Locks the dependencies to specific versions to ensure reproducibility.
- **`data/einakter.json`**: Dataset required for the analysis, symlinked by Nix.

## Building the Project

To build the project, use the following command:

```sh
nix build
```

This will execute the Jupyter notebook and produce the results in the `result` directory.

Alternatively, you can build the project without cloning the repository by using the following command:

```sh
nix build github:v-ji/einakter-chr2024-stats
```

## Developing with Nix

To enter the development environment, use the following command:

```sh
nix develop
```

This will set up the environment with all necessary dependencies and symlink the dataset into the `data` directory.

## Running the Jupyter Notebook

After entering the development environment, you can start the Jupyter Notebook:

```sh
jupyter notebook main.ipynb
```

## Requirements

For non-Nix users, a `requirements.txt` file is provided on a best-effort basis.
However, using Nix is highly recommended for full reproducibility.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
