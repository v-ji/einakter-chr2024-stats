{
  description = "Development environment for the paper ‘Univariate Statistical Analysis of a Non-Canonical Genre’";

  # Flake inputs
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    einakter = {
      url = "https://github.com/dracor-org/einakter/releases/download/v1.5.0/einakter-v1.5.0.json";
      flake = false;
    };
  };

  # Flake outputs
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
    in
    {
      # Development environment output
      devShells = forAllSystems (
        { pkgs }:
        {
          default =
            let
              # Use Python 3.11
              python = pkgs.python311;
            in
            pkgs.mkShell {
              # The Nix packages provided in the environment
              packages = [
                # Python plus helper tools
                (python.withPackages (
                  ps: with ps; [
                    pip # The pip installer
                    jupyter
                    polars # Dataframes
                    pyarrow
                    scipy # Statistics
                    seaborn # Plotting
                  ]
                ))
              ];

              shellHook = ''
                echo "Writing requirements.txt for non-Nix users…"
                echo "# requirements.txt is provided on a best-effort basis." > requirements.txt
                echo "# Please use Nix for a fully reproducible environment." >> requirements.txt
                pip freeze >> requirements.txt

                # Symlink dataset into dev environment (verbose)
                ln -v -f -s ${einakter.outPath} ./data/einakter.json
              '';
            };
        }
      );
    };
}
