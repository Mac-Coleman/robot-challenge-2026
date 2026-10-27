{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
    flake-utils.url = "github:numtide/flake-utils";
  };


  outputs = {
    self,
    nixpkgs,
    flake-utils
  }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {inherit system; config.allowUnfree = true;};
    in
      {
        devShells.default =
        let
          fontsConf = pkgs.makeFontsConf {
            fontDirectories = [
              pkgs.font-bh-lucidatypewriter-100dpi
            ];
          };
        in
          pkgs.mkShell {
            packages = with pkgs; [
              python3
              python3Packages.pygame
            ];
            shellHook = ''
              export FONTCONFIG_FILE="${fontsConf}"
            '';
          };
      }
  );
}
