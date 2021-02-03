from pathlib import Path
import hashlib
from  {{cookiecutter.package_name}}.utils.ftp import FtpUtil


def hash_local(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def determine_files_to_copy(local_folder, remote_details):
    folder = Path(local_folder)
    local_files = {}
    for file in folder.iterdir():
        if file.is_file():
            local_files[file.name] = hash_local(folder / file)

    ftp = FtpUtil(**remote_details)
    remote_files = {}
    for rm_file in ftp.ls():
        if not rm_file == "." and not rm_file == "..":
            remote_files[rm_file] = ftp.md5("/", rm_file)

    to_copy = []

    for file_on_ftp in remote_files.keys():
        if file_on_ftp in local_files.keys():
            if local_files[file_on_ftp] != remote_files[file_on_ftp]:
                to_copy.append({
                    "name": file_on_ftp,
                    "status": "changed"
                })
        else:
            to_copy.append({
                "name": file_on_ftp,
                "status": "new"
            })
    return to_copy


def synchronize_ftp(local_folder, remote_details):
    files = determine_files_to_copy(local_folder, remote_details)

    if files:
        ftp = FtpUtil(**remote_details)
        for file in files:
            ftp.download("/", local_folder, file["name"])

    return files
