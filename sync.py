import os
import sys
import time

# Save colors in constants to decorate the console output
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
END = '\033[0m'


# **********************************************************************************
# Function log_write()
# **********************************************************************************
def log_write(log):
    log_file = log_file_path + "sync_log.txt"

    try:
        with open(log_file, "a") as log_file:
            log_file.write(log)
            # Comment next line to supress console output
            print(log.strip('\n'))
    except Exception:
        with open(log_file, "w+") as log_file:
            log_file.write(f" ******* Log ******\n\n")
            print(log.strip('\n'))


# **********************************************************************************
# Function file_write()
# **********************************************************************************
def file_write(source_path, mirror_path):
    with open(source_path, "rb") as src_file, open(mirror_path, "wb") as dst_file:
        dst_file.write(src_file.read())
        log_write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {GREEN}Update file:{END} {mirror_path}\n")


# **********************************************************************************
# Function copy_folder
# **********************************************************************************
def copy_folder(src_path, dst_path):
    # Copy each file from the source directory to the destination directory
    for file_name in os.listdir(src_path):
        source_path = os.path.join(src_path, file_name)
        mirror_path = os.path.join(dst_path, file_name)
        # If the file path is a folder, call this function recursively to navigate the folders tree
        if os.path.isdir(mirror_path):
            copy_folder(source_path, mirror_path)

        # Create the destination folder if it doesn't exist
        if not os.path.exists(mirror_path):
            # If the file path is a folder, call this function recursively to navigate the folders tree
            if os.path.isdir(source_path):
                os.makedirs(mirror_path)
                log_write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {GREEN}Create folder: {END}{dst_path}")
                copy_folder(source_path, mirror_path)

        # Create/update the destination file if it doesn't exist or has been modified
        if os.path.isfile(source_path):
            if not os.path.exists(mirror_path):
                file_write(source_path, mirror_path)

            # Check if file has been modified (sync script is deleting and create another)
            elif os.stat(mirror_path).st_mtime != os.stat(mirror_path).st_ctime:
                file_write(source_path, mirror_path)

            # Check if source file has been updated
            elif os.stat(mirror_path).st_mtime < os.stat(source_path).st_mtime:
                file_write(source_path, mirror_path)

            # Safety check if size is different
            elif os.path.getsize(source_path) != os.path.getsize(mirror_path):
                file_write(source_path, mirror_path)

                file_write(source_path, mirror_path)





# **********************************************************************************
# Function delete_folder()
# **********************************************************************************
def delete(source, mirror):
    # Loop through all the files and folders in the directory
    for file_name in os.listdir(mirror):
        source_path = os.path.join(source, file_name)
        mirror_path = os.path.join(mirror, file_name)
        # If the file path is a folder, call this function recursively to navigate the folders tree
        if os.path.isdir(mirror_path):
            delete(source_path, mirror_path)
        if not os.path.exists(source_path):
            if os.path.isdir(mirror_path):
                remove_folder(mirror_path)
                log_write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {BLUE}Removed file: {END}{mirror_path}\n")

            elif os.path.isfile(mirror_path):
                os.remove(mirror_path)
                log_write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {BLUE}Removed file: {END}{mirror_path}\n")


# **********************************************************************************
# Function remove_folder()
# **********************************************************************************
def remove_folder(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            # Loop through all the files and folders in the directory
            for file_name in os.listdir(path):
                file_path = os.path.join(path, file_name)
                # If the file path is a folder, call this function recursively to navigate the folders tree
                if os.path.isdir(file_path):
                    remove_folder(file_path)
                    log_write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {BLUE}Removed folder: {END}{file_path}\n")
                # If the file path is a file, delete it
                else:
                    os.remove(file_path)
                    log_write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {BLUE}Removed file: {END}{file_path}\n")
            # After deleting all the files and folders in the directory, remove the directory itself
            os.rmdir(path)
            log_write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {BLUE}Removed folder: {END}{path}\n")



# **********************************************************************************
# Function schedule
# **********************************************************************************
def schedule(sch_interval):
    while True:
        # Check for modification and update copy all modified files
        copy_folder(src_path, dst_path)

        # Delete  all destination files/folders if they don't exist in source
        delete(src_path, dst_path)
        try:

            # Check for modification and update copy all modified files
            copy_folder(src_path, dst_path)

            # Delete  all destination files/folders if they don't exist in source
            delete(src_path, dst_path)

        except Exception as e:
            log_write(f"{RED}{time.strftime('%Y-%m-%d %H:%M:%S')} - Error  folder: {e}{END}\n")
        log_write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Update successful.\n")
        time.sleep(sch_interval)


# **********************************************************************************
# main block
# **********************************************************************************


'''
sch_interval = ''
src_path = ''
dst_path = ''
log_file_path = ''
'''

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: sync.py <source_folder> <target_folder> <log_folder> <sync_interval(hh:mm:ss)>")
        sys.exit(1)
    src_path = sys.argv[1]
    dst_path = sys.argv[2]
    log_file_path = sys.argv[3]
    sch_interval = sys.argv[4]
    error_argv = False

    # Argv errors
    if not os.path.isdir(src_path) or not os.path.isdir(src_path) or not os.path.isdir(log_file_path):
        log_write(f"{RED}{time.strftime('%Y-%m-%d %H:%M:%S')} -{src_path} is not a folder: {END}\n")
        error_argv = True

    elif not os.access(src_path, os.R_OK):
        log_write(f"{RED}{time.strftime('%Y-%m-%d %H:%M:%S')} -Read permission is denied in {src_path} folder: {END}\n")
        error_argv = True

    elif not os.access(dst_path, os.W_OK):
        log_write(
            f"{RED}{time.strftime('%Y-%m-%d %H:%M:%S')} -Write permission is denied in {dst_path} folder: {END}\n")
        error_argv = True

    elif not os.access(log_file_path, os.W_OK):
        log_write(
            f"{RED}{time.strftime('%Y-%m-%d %H:%M:%S')} -Write permission is denied in {log_file_path} folder: {END}\n")
        error_argv = True

    elif not os.path.relpath(src_path, dst_path).startswith('..') or src_path == dst_path:
        log_write(
            f"{RED}{time.strftime('%Y-%m-%d %H:%M:%S')} -{dst_path} is a subfolder of  {src_path} folder: {END}\n")
        error_argv = True

    elif not os.path.relpath(dst_path, src_path).startswith('..'):
        log_write(
            f"{RED}{time.strftime('%Y-%m-%d %H:%M:%S')} -{src_path} is a subfolder of  {src_path} folder: {END}\n")
        error_argv = True

    # *****************************************************************************************************
    # Set CHMOD 733 to source and mirror file to avoid restricted access files or subfolders
    # Comment all try if CHMOD is not desired
    # *****************************************************************************************************
    try:

        # Set CHMOD 733 to SOURCE folder and all files and subfolders. Modify next line for different setting
        chm_source = 0o733
        # Set CHMOD 733 to MIRROR folder and all files and subfolders. Modify next line for different setting
        chm_mirror = 0o733

        # Set CHMOD 733 to SOURCE folder and all files and subfolders.
        for dirpath, dirnames, filenames in os.walk(src_path):
            for dirname in dirnames:
                dir_full_path = os.path.join(dirpath, dirname)
                os.chmod(dir_full_path, chm_source)
            for filename in filenames:
                file_full_path = os.path.join(dirpath, filename)
                os.chmod(file_full_path, chm_source)

        # Set CHMOD 733 to MIRROR folder and all files and subfolders.
        for dirpath, dirnames, filenames in os.walk(src_path):
            for dirname in dirnames:
                dir_full_path = os.path.join(dirpath, dirname)
                os.chmod(dir_full_path, chm_mirror)
            for filename in filenames:
                file_full_path = os.path.join(dirpath, filename)
                os.chmod(file_full_path, chm_mirror)
        log_write(f"{GREEN}{time.strftime('%Y-%m-%d %H:%M:%S')} Set CHMOD {chm_source} to SOURCE folder:{src_path} {END}\n")
        log_write(f"{GREEN}{time.strftime('%Y-%m-%d %H:%M:%S')} Set CHMOD {chm_source} to SOURCE folder:{src_path} {END}\n")

    except Exception as c:
        log_write(f"{RED}{time.strftime('%Y-%m-%d %H:%M:%S')} WARNING:Set CHMOD ERROR {END}\n")
        error_argv = True

    # *****************************************************************************************************


    if error_argv:
        print("Usage: sync.py <source_folder> <target_folder> <log_folder> <sync_interval(hh:mm:ss)>")
        sys.exit(1)

    # Warnings and default setup
    try:
        sch_interval = sch_interval.strip().lower().split(":")
        hh, mm, ss = sch_interval[0], sch_interval[1], sch_interval[2]
        if hh == '':
            hh = 0
        else:
            hh = int(hh)
        if mm == '':
            mm = 0
        else:
            mm = int(mm)
        if ss == '':
            ss = 0
        else:
            ss = int(ss)
        sch_interval = hh * 3600 + mm * 60 + ss
        if sch_interval == 0:
            sch_interval = 24 * 3600
    except Exception as e:
        log_write(
            f"{RED}{time.strftime('%Y-%m-%d %H:%M:%S')} Error sync interval Default 24H was enable: {END}\n")

    try:
        schedule(sch_interval)
    except KeyboardInterrupt:
        print("Goodbye")
        exit(0)
