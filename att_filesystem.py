import subprocess
from datetime import date

def att_filesystem():
    
    user_name = "servidor_lib"

    now = date.now()
    time = now.strftime("%b-%d-%Y-%Hh-%mm-%Ss")

    backup_path = f"/home/{user_name}/backup/filesystems/B_filesystem_{time}.squashfs"
    destin_path = "/nfsroot/pxefiles/casper/filesystem.squashfs"
    in_path = f"/home/{user_name}/squashfs-root"
    out_path = f"/home/{user_name}/filesystem.squashfs"

    backup_cmd = "cp"
    mksquash_cmd = "sudo mksquashfs"
    move_squash = "mv"

    st_backup = subprocess.run([backup_cmd, destin_path, backup_path])

    if st_backup.returncode==0:
        st_mksquash = subprocess.run([mksquash_cmd, in_path, out_path])
        if st_mksquash.returncode==0:
            st_mvsquash = subprocess.run([move_squash, out_path, destin_path])

    return st_backup.returncode,st_mksquash.returncode,st_mvsquash.returncode