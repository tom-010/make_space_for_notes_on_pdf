{ pkgs ? import <nixpkgs> {
  # Enable the installation of unfree packages
  config = {
    allowUnfree = true;
  };
} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    gcc
    python3
    zsh
    tmux
    vscode
    zlib.dev
  ];

  shellHook = ''

    # Set the shell =================================================
    export SHELL=${pkgs.zsh}/bin/zsh
    export TMPDIR=/var/tmp # to avoid python and pip oom errors: https://superuser.com/questions/1288308/why-am-i-getting-no-space-left-on-device-when-it-appears-that-theres-lots-of
    source $(poetry env info --path)/bin/activate # instead of poetry shell
    export PYTHONPATH=.
    
    # Setup the environment =========================================
    
    ## gcc, c and c++ libraries
    export LD_LIBRARY_PATH="${pkgs.gcc}/lib:${pkgs.gcc}/lib64:${pkgs.zlib}/lib:$LD_LIBRARY_PATH"



    # Initialize tmux =============================================== 

    # Prepare the tmux project layout ==============================

    # Get the name of the current directory to use as the tmux session name
    SESSION_NAME=$(basename "$(pwd)")

    if [ -z "$TMUX" ]; then

      # Window: Code editing
      tmux -L "$SESSION_NAME" 
    fi

    exec ${pkgs.zsh}/bin/zsh
  '';
}


