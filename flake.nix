{
  description = "Unofficial CLI for the fckaf.de URL shortener";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/26.05";

  outputs = { self, nixpkgs }:
    let
      forAllSystems = nixpkgs.lib.genAttrs nixpkgs.lib.systems.flakeExposed;
      fckafdeFor = system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          pythonEnv = pkgs.python3.withPackages (ps: [ ps.requests ps.lxml ]);
        in
        pkgs.writeShellScriptBin "fckafde" ''
          exec ${pythonEnv}/bin/python3 ${./fck.py} "$@"
        '';
    in {
      packages = forAllSystems (system: {
        default = fckafdeFor system;
        fckafde-cli = fckafdeFor system;
      });
      apps = forAllSystems (system: {
        default = {
          type = "app";
          program = "${fckafdeFor system}/bin/fckafde";
        };
      });
    };
}
