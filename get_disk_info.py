#!/usr/bin/env python3
import subprocess
from textwrap import dedent

HOST = "root@100.74.250.48"   # change if needed

# Minimal remote script: print a clean table with what we can get.
REMOTE_SCRIPT = dedent(r"""
    #!/usr/bin/env bash
    shopt -s nullglob

    printf "%-12s %-16s %-6s %-28s %10s %10s %10s %14s\n" \
        "MOUNT" "SOURCE" "FS" "SERIAL" "%USED" "ACTUAL" "IDEAL" "FRAG(%)"
    printf "%-12s %-16s %-6s %-28s %10s %10s %10s %14s\n" \
        "------------" "----------------" "------" "----------------------------" "----------" "----------" "----------" "--------------"

    list_mounts() {
      for mp in /mnt/disk* /mnt/cache*; do
        [ -d "$mp" ] && mountpoint -q "$mp" && echo "$mp"
      done
    }

    dev_for_mount() { findmnt -no SOURCE --target "$1" 2>/dev/null; }
    fs_for_mount()  { findmnt -no FSTYPE --target "$1" 2>/dev/null; }

    # For /dev/mdX find real /dev/sdX (first slave)
    physical_device_for() {
      local src="$1"; local base="${src##*/}"
      if [[ "$base" == md* ]]; then
        for s in /sys/block/"$base"/slaves/*; do
          [ -e "$s" ] || continue
          echo "/dev/$(basename "$s")"; return
        done
      fi
      if [[ "$src" =~ ^/dev/ ]]; then echo "$src"; else echo ""; fi
    }

    serial_for_device() {
      local dev="$1"
      [ -n "$dev" ] || { echo ""; return; }
      udevadm info --query=property --name "$dev" 2>/dev/null \
        | awk -F= '$1=="ID_SERIAL"{print $2; exit}'
    }

    util_pct() {
      df -P "$1" 2>/dev/null | awk 'NR==2 && $2>0 {printf "%.2f", ($3/$2)*100}'
    }

    xfs_frag() {
      local dev="$1"
      [ -n "$dev" ] || { echo "||"; return; }
      local o; o="$(xfs_db -r "$dev" -c frag 2>/dev/null)" || { echo "||"; return; }
      local a i p
      a="$(awk -F'[ ,]+' '/actual/{print $2}' <<<"$o")"
      i="$(awk -F'[ ,]+' '/ideal/{print $4}' <<<"$o")"
      p="$(awk -F'[ %]+' '/fragmentation/{print $4}' <<<"$o")"
      echo "${a}|${i}|${p}"
    }

    zfs_frag_pct_for_mount() {
      command -v zfs >/dev/null 2>&1 || { echo ""; return; }
      command -v zpool >/dev/null 2>&1 || { echo ""; return; }
      local mp="$1" dataset pool pct
      dataset="$(zfs list -H -o name,mountpoint 2>/dev/null | awk -v m="$mp" '$2==m{print $1; exit}')"
      [ -n "$dataset" ] || { echo ""; return; }
      pool="${dataset%%/*}"
      pct="$(zpool get -H -p fragmentation "$pool" 2>/dev/null | awk '{print $3}' | tr -d '%')"
      echo "$pct"
    }

    for mp in $(list_mounts); do
      src="$(dev_for_mount "$mp")"
      fs="$(fs_for_mount "$mp")"
      used="$(util_pct "$mp")"

      serial=""; act=""; ideal=""; frag=""

      if [ "$fs" = "xfs" ]; then
        phy="$(physical_device_for "$src")"
        serial="$(serial_for_device "$phy")"
        IFS="|" read -r act ideal frag <<<"$(xfs_frag "$phy")"
      elif [ "$fs" = "zfs" ]; then
        frag="$(zfs_frag_pct_for_mount "$mp")"
        serial=""
      else
        phy="$(physical_device_for "$src")"
        serial="$(serial_for_device "$phy")"
      fi

      printf "%-12s %-16s %-6s %-28s %10s %10s %10s %14s\n" \
        "$mp" "${src:0:16}" "${fs:0:6}" "${serial:0:28}" \
        "${used:-}" "${act:-}" "${ideal:-}" "${frag:-}"
    done
""").lstrip()

def main():
    # This will stream output directly to your terminal (no JSON/files).
    # If SSH needs a password, your terminal will prompt interactively.
    cmd = ["ssh", HOST, "bash -s"]
    try:
        subprocess.run(cmd, input=REMOTE_SCRIPT.encode(), check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nSSH/remote error (exit {e.returncode}). "
              f"Make sure you can SSH to {HOST} from this terminal (try: ssh {HOST}).")

if __name__ == "__main__":
    main()
