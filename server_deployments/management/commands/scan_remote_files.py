import os
import paramiko
import time
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from server_deployments.models import IndexedFolder, IndexedFile, System


def load_env(filepath=".env"):
    if not os.path.exists(filepath):
        print(f"Warning: .env file not found at {filepath}")
        return
    with open(filepath) as f:
        for line in f:
            if not line.strip() or line.strip().startswith("#"):
                continue
            key, _, value = line.strip().partition("=")
            os.environ.setdefault(key, value)


class Command(BaseCommand):
    help = "Scans remote files on a given system and updates IndexedFolder and IndexedFile"

    def handle(self, *args, **options):
        load_env()

        SSH_HOST = os.environ['SSH_HOST']
        SSH_USER = os.environ['SSH_USER']
        SSH_PASSWORD = os.environ['SSH_PASSWORD']
        SYSTEM_ID = int(os.environ['SCAN_SYSTEM_ID'])
        TARGET_DIR = "/mnt/user/"

        start_time_str = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"Scan started at {start_time_str}")

        ssh = self.ssh_connect(SSH_HOST, SSH_USER, SSH_PASSWORD)

        print(f"Running: find {TARGET_DIR} -type f -exec du -b {{}} +")
        command = f'find "{TARGET_DIR}" -type f -exec du -b {{}} +'
        stdin, stdout, stderr = ssh.exec_command(command)

        stdout_lines = []
        print("Streaming remote file list...")

        start_stream = time.time()
        last_print = start_stream

        for i, line in enumerate(stdout, 1):
            stdout_lines.append(line)

            if i % 1000 == 0:
                elapsed = round(time.time() - last_print, 1)
                total_elapsed = round(time.time() - start_stream, 1)
                print(f"  -> {i} files found... ({elapsed}s since last update, {total_elapsed}s total)")
                last_print = time.time()

        print(f"\nFinished streaming. Total files: {len(stdout_lines)}")

        stderr_lines = stderr.readlines()
        if stderr_lines:
            print("\nErrors:")
            for line in stderr_lines:
                print(line.strip())

        if not stdout_lines:
            print("No files found.")
            return

        parsed_files = self.parse_find_output(stdout_lines)
        system = System.objects.get(id=SYSTEM_ID)

        folder_map = {}
        for file_data in parsed_files:
            folder_path = os.path.dirname(file_data['full_path'])
            folder_map.setdefault(folder_path, []).append(file_data)

        folders_created = 0
        files_written = 0
        total_folders = len(folder_map)

        print(f"\n--- Writing to database ({total_folders} folders) ---")
        start_write_time = time.time()
        last_report_time = start_write_time

        for i, (folder_path, file_list) in enumerate(folder_map.items(), 1):
            print(f"-> [{i}/{total_folders}] {folder_path} ({len(file_list)} files)")

            folder, created = IndexedFolder.objects.get_or_create(system=system, path=folder_path)
            if created:
                folders_created += 1

            folder.total_size = sum(f['file_size'] for f in file_list)
            folder.last_scanned = now()
            folder.save()

            for j, f in enumerate(file_list, 1):
                _, created = IndexedFile.objects.update_or_create(
                    system=system,
                    full_path=f['full_path'],
                    defaults={
                        'folder': folder,
                        'filename': f['filename'],
                        'file_size': f['file_size'],
                        'file_type': f['file_type'],
                        'last_scanned': now(),
                    }
                )
                files_written += 1

                if j == 1 or j % 500 == 0:
                    print(f"    [{j}/{len(file_list)}] {f['full_path']}")

            current_time = time.time()
            if current_time - last_report_time >= 10 or i == total_folders:
                elapsed = round(current_time - start_write_time, 1)
                print(f"Progress: {i}/{total_folders} folders | {files_written} files | {elapsed}s elapsed")
                last_report_time = current_time

        total_time = round(time.time() - start_write_time, 1)
        print("\nDatabase update complete.")
        print(f"Folders created: {folders_created}")
        print(f"Files added/updated: {files_written}")
        print(f"Write duration: {total_time}s")

        ssh.close()

    def ssh_connect(self, host, user, password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"Connecting to {user}@{host}...")
            ssh.connect(hostname=host, username=user, password=password, timeout=10)
            print("SSH connection successful.")
            return ssh
        except paramiko.AuthenticationException:
            print("Authentication failed. Check SSH_USER and SSH_PASSWORD.")
            raise
        except paramiko.SSHException as e:
            print(f"SSH connection error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def parse_find_output(self, lines):
        print("Parsing SSH output...")
        parsed = []
        for i, line in enumerate(lines):
            try:
                size_str, full_path = line.strip().split(None, 1)
                size = int(size_str)
                filename = os.path.basename(full_path)
                ext = os.path.splitext(filename)[1].lstrip('.').lower()
                parsed.append({
                    "full_path": full_path,
                    "filename": filename,
                    "file_size": size,
                    "file_type": ext
                })
                if i % 5000 == 0:
                    print(f"Parsing: {full_path}")
            except Exception as e:
                print(f"Skipping malformed line [{line.strip()}]: {e}")
        return parsed
