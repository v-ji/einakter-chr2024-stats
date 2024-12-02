{
  description = "Development environment for the paper ‘Univariate Statistical Analysis of a Non-Canonical Genre’";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    einakter = {
      url = "https://github.com/dracor-org/einakter/releases/download/v2.0.0/einakter-v2.0.0.json";
      flake = false;
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      einakter,
    }:
    let
      # Systems supported
      defaultSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      # Helper to provide system-specific attributes
      forAllSystems =
        f: nixpkgs.lib.genAttrs defaultSystems (system: f { pkgs = import nixpkgs { inherit system; }; });

      pythonVersion = pkgs: pkgs.python312;

      # Define Python packages
      getPythonPackages =
        pkgs: ps: with ps; [
          jupyter
          polars
          pyarrow
          scipy
          seaborn
        ];

      # Create Python environment
      getPythonEnv =
        pkgs: extraPackages:
        (pythonVersion pkgs).withPackages (ps: getPythonPackages pkgs ps ++ extraPackages ps);
    in
    {
      devShells = forAllSystems (
        { pkgs }:
        {
          default = pkgs.mkShell {
            packages = [ (getPythonEnv pkgs (ps: [ ps.pip ])) ];
            EINAKTER_DATASET_PATH = einakter.outPath;
            shellHook = ''
              echo "Writing requirements.txt for non-Nix users…"
              echo "# requirements.txt is provided on a best-effort basis." > requirements.txt
              echo "# Please use Nix for a fully reproducible environment." >> requirements.txt
              pip freeze >> requirements.txt
            '';
          };
        }
      );

      packages = forAllSystems (
        { pkgs, ... }:
        {
          default = pkgs.stdenv.mkDerivation {
            name = "jupyterNotebook";
            src = ./.;

            # Required for the Jupyter server to work on macOS
            __darwinAllowLocalNetworking = true;

            buildInputs = [ (getPythonEnv pkgs (ps: [ ])) ];

            EINAKTER_DATASET_PATH = einakter.outPath;

            buildPhase = ''
              # Create a directory for the matplotlib configuration (suppresses warning)
              export MPLCONFIGDIR=$(pwd)/matplotlib

              echo "Executing Jupyter notebook…"

              jupyter nbconvert \
                --to notebook \
                --execute \
                --ClearMetadataPreprocessor.enabled=True \
                --output result \
                main.ipynb

              echo "Rendering Jupyter notebook to HTML…"

              jupyter nbconvert \
                --to html \
                result.ipynb
            '';

            installPhase = ''
              mkdir -p $out
              cp result.ipynb $out/
              cp result.html $out/
              cp -r outputs/ $out/
            '';
          };
        }
      );
    };
}
