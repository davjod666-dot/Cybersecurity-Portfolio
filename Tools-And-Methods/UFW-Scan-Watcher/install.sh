#!/usr/bin/env bash
set -euo pipefail
source_dir=$(cd -- "$(dirname -- "$0")" && pwd)
/usr/bin/python3 -m unittest discover -s "$source_dir" -v
journalctl -k -n 1 --no-pager >/dev/null
command -v notify-send >/dev/null
mkdir -p "$HOME/.local/bin" "$HOME/.config/systemd/user"
backup_stamp=$(date +%Y%m%d-%H%M%S)
for target in "$HOME/.local/bin/portfolio-scan-watcher.py" "$HOME/.config/systemd/user/ufw-scan-watcher.service"; do
    if [[ -e "$target" ]]; then cp -a -- "$target" "$target.backup-$backup_stamp"; fi
done
install -m 755 "$source_dir/scan_watcher.py" "$HOME/.local/bin/portfolio-scan-watcher.py"
install -m 644 "$source_dir/ufw-scan-watcher.service" "$HOME/.config/systemd/user/ufw-scan-watcher.service"
systemctl --user daemon-reload
systemctl --user enable ufw-scan-watcher.service
# Restart also starts an inactive service and loads updated code on reinstall.
systemctl --user restart ufw-scan-watcher.service
systemctl --user is-active ufw-scan-watcher.service
journalctl --user -u ufw-scan-watcher.service -n 10 --no-pager
notify-send -a 'UFW scan watcher' 'Watcher notification check' 'Installation check only; this is not a detected scan.'
