{pkgs}: {
  deps = [
    pkgs.redis
    pkgs.wget
    pkgs.systemd
    pkgs.mysql84
    pkgs.vim
  ];
}
