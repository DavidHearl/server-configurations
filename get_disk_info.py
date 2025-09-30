#!/usr/bin/env python3
import subprocess
from textwrap import dedent
import os
import sys
import django
import re

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server_configurations.settings')
django.setup()

from server_deployments.models import StorageDevice, System

HOST = "root@100.74.250.48"   # change if needed

# Modified remote script to output JSON-like format for easier parsing
REMOTE_SCRIPT = dedent(r"""
    #!/usr/bin/env bash
    shopt -s nullglob

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

    # Output in parseable format: MOUNT|SOURCE|FS|SERIAL|USED|ACTUAL|IDEAL|FRAG
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

      echo "DATA|$mp|$src|$fs|$serial|$used|$act|$ideal|$frag"
    done
""").lstrip()

def parse_disk_number(mount_point):
    """Extract disk number from mount point like /mnt/disk1 -> 1"""
    match = re.search(r'/mnt/disk(\d+)', mount_point)
    if match:
        return int(match.group(1))
    return None

def update_storage_devices():
    """Run the remote script and update storage devices in database"""
    print("Fetching disk information from Unraid server...")
    
    # Get the Plex system (assuming there's only one or it's identifiable)
    try:
        plex_system = System.objects.get(name__icontains='plex')
        print(f"Found Plex system: {plex_system.name}")
    except System.DoesNotExist:
        print("Error: Could not find Plex system in database. Please create it first.")
        return
    except System.MultipleObjectsReturned:
        print("Error: Multiple Plex systems found. Please specify which one to use.")
        return
    
    # Run the remote script  
    cmd = ["ssh", HOST, "bash -s"]
    try:
        result = subprocess.run(cmd, input=REMOTE_SCRIPT.encode('utf-8'), capture_output=True, check=True)
        output_lines = result.stdout.decode('utf-8').strip().split('\n')
        
        updated_count = 0
        created_count = 0
        
        for line in output_lines:
            if not line.startswith('DATA|'):
                continue
                
            # Parse the data line
            parts = line[5:].split('|')  # Remove 'DATA|' prefix
            if len(parts) < 8:
                continue
                
            mount_point, source, fs_type, serial, used, actual, ideal, frag = parts
            
            # Extract disk number
            disk_number = parse_disk_number(mount_point)
            if disk_number is None:
                print(f"Could not parse disk number from {mount_point}")
                continue
            
            print(f"Processing disk {disk_number} from {mount_point}")
            
            # Try to find existing storage device by disk location in the Plex system
            try:
                storage_device = plex_system.storage_devices.get(disk_location=disk_number)
                print(f"  Found existing device at disk location {disk_number}: {storage_device.model}")
                created = False
            except StorageDevice.DoesNotExist:
                print(f"  No storage device found at disk location {disk_number} in Plex system")
                continue  # Skip if no matching device found
            
            # Update the fragmentation and utilization data
            if used:
                try:
                    storage_device.utilisation = float(used)
                    print(f"  Updated utilization: {used}%")
                except ValueError:
                    pass
            
            if actual:
                try:
                    storage_device.actual_fragmentation = int(actual)
                    print(f"  Updated actual fragmentation: {actual}")
                except ValueError:
                    pass
            
            if ideal:
                try:
                    storage_device.ideal_fragmentation = int(ideal)
                    print(f"  Updated ideal fragmentation: {ideal}")
                except ValueError:
                    pass
            
            if frag:
                try:
                    storage_device.fragmentation = float(frag)
                    print(f"  Updated fragmentation percentage: {frag}%")
                except ValueError:
                    pass
            
            storage_device.save()
            updated_count += 1
            print(f"  Successfully updated disk {disk_number}")
        
        plex_system.save()
        print(f"\nSummary:")
        print(f"  Created: {created_count} new storage devices")
        print(f"  Updated: {updated_count} existing storage devices")
        
    except subprocess.CalledProcessError as e:
        print(f"SSH/remote error (exit {e.returncode}). "
              f"Make sure you can SSH to {HOST} from this terminal (try: ssh {HOST}).")
        print(f"Error output: {e.stderr}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Update storage device information from Unraid')
    parser.add_argument('--show-only', action='store_true', 
                       help='Only show disk information without updating database')
    
    args = parser.parse_args()
    
    if args.show_only:
        # Original behavior - just show the information
        cmd = ["ssh", HOST, "bash -s"]
        try:
            subprocess.run(cmd, input=REMOTE_SCRIPT.encode('utf-8'), check=True)
        except subprocess.CalledProcessError as e:
            print(f"\nSSH/remote error (exit {e.returncode}). "
                  f"Make sure you can SSH to {HOST} from this terminal (try: ssh {HOST}).")
    else:
        # Default behavior - update the database
        update_storage_devices()

if __name__ == "__main__":
    main()