import tarfile
import os
import datetime

def backup(backup_dir="/tmp/backup", src_dir="/tmp/test", backup_filename=None):
    if not backup_filename:
        backup_filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".tar.gz"
    
    backup_fullpath = os.path.join(backup_dir, backup_filename)
    with tarfile.open(backup_fullpath, "w:gz") as tar:
        tar.add(src_dir)

if __name__ == "__main__":
    backup()
