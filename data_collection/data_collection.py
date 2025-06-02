import os
import sys

# Django setup (must come before importing models)
sys.path.append('/Users/davidhearl/Documents/08 - Programming/GitHub/server_configurations')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server_configurations.settings')
import django
django.setup()

from server_deployments.models import *
from django.utils.timezone import now
import paramiko
import time
from datetime import datetime

system = System.objects.get(name='Plex - Movies')


def load_env(file_path='.env'):
    with open(file_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

def ssh_connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    hostname = os.environ['SSH_HOST']
    username = os.environ['SSH_USER']
    password = os.environ.get('SSH_PASSWORD')
    key_path = os.environ.get('SSH_KEY')

    if key_path:
        client.connect(hostname, username=username, key_filename=key_path)
    else:
        client.connect(hostname, username=username, password=password)
    
    return client

def get_folder_info(client, folder_path):
    """Returns the total size (bytes) and file count for a folder."""
    size_command = f'du -sb "{folder_path}" | cut -f1'
    count_command = f'find "{folder_path}" -type f | wc -l'

    stdin, stdout, _ = client.exec_command(size_command)
    size = int(stdout.read().decode().strip())

    stdin, stdout, _ = client.exec_command(count_command)
    file_count = int(stdout.read().decode().strip())

    return size, file_count

def scan_movies(client, path, system):
    command = f'find "{path}" -mindepth 1 -maxdepth 1 -type d'
    stdin, stdout, _ = client.exec_command(command)
    folders = stdout.read().decode().strip().split('\n')

    for folder in folders:
        if folder:
            size, count = get_folder_info(client, folder)
            MovieIndex.objects.update_or_create(
                system=system,
                path=folder,
                defaults={
                    'name': os.path.basename(folder),
                    'file_count': count,
                    'folder_size_bytes': size,
                    'last_scanned': now()
                }
            )


def scan_tv_programs(client, path, system):
    command = f'find "{path}" -mindepth 1 -maxdepth 1 -type d'
    stdin, stdout, _ = client.exec_command(command)
    shows = stdout.read().decode().strip().split('\n')

    for show in shows:
        if not show:
            continue

        season_command = f'find "{show}" -mindepth 1 -maxdepth 1 -type d'
        stdin, stdout, _ = client.exec_command(season_command)
        seasons = stdout.read().decode().strip().split('\n')

        total_size = 0
        tv_show_obj, _ = TVShowIndex.objects.update_or_create(
            system=system,
            path=show,
            defaults={
                'name': os.path.basename(show),
                'season_count': len(seasons),
                'total_size_bytes': 0,  # Will update later
                'last_scanned': now()
            }
        )

        for season in seasons:
            if season:
                size, count = get_folder_info(client, season)
                total_size += size

                SeasonIndex.objects.update_or_create(
                    path=season,
                    defaults={
                        'tv_show': tv_show_obj,
                        'name': os.path.basename(season),
                        'file_count': count,
                        'folder_size_bytes': size
                    }
                )

        tv_show_obj.total_size_bytes = total_size
        tv_show_obj.save()


# --- MAIN EXECUTION ---

if __name__ == '__main__':
    print(f"\n🕒 Scan started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    load_env()
    client = ssh_connect()

    try:
        start = time.time()
        scan_movies(client, '/mnt/user/Media/Movies', system)  # Pass system here
        scan_tv_programs(client, '/mnt/user/Media/TV Programs', system)  # And here
        print(f"\n✅ Total scan time: {time.time() - start:.2f}s")
    finally:
        client.close()
        print("\n🔌 SSH connection closed.")
