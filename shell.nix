let
  pkgs = import <nixpkgs> {};
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    (python3.withPackages (python-packages: with python-packages; [
        flask jsonschema
      ]))
  ];
}
