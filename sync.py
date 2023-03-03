import os
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
    with open(log_file_path, "a") as log_file:
        log_file.write(log)
        # Comment next line to supress console output
        print(log.strip('\n'))


# **********************************************************************************
# Function file_write()
# **********************************************************************************
def file_write(source_path, mirror_path):
    with open(source_path, "rb") as src_file, open(mirror_path, "wb") as dst_file:
        chunk_size = 1024 * 1024  # 1MB
        while True:
            chunk = src_file.read(chunk_size)
            if not chunk:
                break
            dst_file.write(chunk)
    log_write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {GREEN}Update file:{END} {mirror_path}\n")


# **********************************************************************************
# Function copy_folder
# **********************************************************************************
def copy_folder(src_path, dst_path):
    try:
        # Copy each file from the source directory to the destination directory
        for file_name in os.listdir(src_path):
            source_path = os.path.join(src_path, file_name)
            mirror_path = os.path.join(dst_path, file_name)
            # print('source -',source_path)
            # print('miror = ',mirror_path)

            # Create the destination folder if it doesn't exist
            if not os.path.exists(mirror_path):
                if os.path.isdir(source_path):
                    os.makedirs(mirror_path)
                    log_write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {GREEN}Create folder: {END}{dst_path}")
                    copy_folder(source_path, mirror_path)

            # Create/update the destination file if it doesn't exist or has been modified
            if os.path.isfile(source_path):
                if not os.path.exists(mirror_path):
                    file_write(source_path, mirror_path)
                elif os.path.getmtime(source_path) > os.path.getmtime(mirror_path):
                    file_write(source_path, mirror_path)
                elif os.path.getsize(source_path) != os.path.getsize(mirror_path):
                    file_write(source_path, mirror_path)

            # Create a symbolic link at dst_path pointing to link_target
            elif os.path.islink(source_path):
                link_target = os.readlink(source_path)
                os.symlink(link_target, os.path.join(dst_path, os.path.basename(source_path)))


    except Exception as e:
        log_write(f"{RED}{time.strftime('%Y-%m-%d %H:%M:%S')} - Error copying folder: {e}\n{END}")


# **********************************************************************************
# Function delete_folder()
# **********************************************************************************
def delete(source, mirror):
    for file_name in os.listdir(mirror):
        #print(file_name)
        source_path = os.path.join(source, file_name)
        mirror_path = os.path.join(mirror, file_name)
        if not os.path.exists(source_path):
            #print("remove")
            if os.path.isdir(mirror_path):
                remove_folder(mirror_path)

            elif os.path.isfile(mirror_path):
                os.remove(mirror_path)
                log_write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {BLUE}Removed file: {END}{mirror_path}\n")


# **********************************************************************************
# Function remove_folder()
# **********************************************************************************
def remove_folder(path):
    # Check if the given path exists
    if os.path.exists(path):
        # Check if the given path is a directory
        if os.path.isdir(path):
            # Loop through all the files and folders in the directory
            for file_name in os.listdir(path):
                # Construct the full file path
                file_path = os.path.join(path, file_name)
                # If the file path is a directory, call this function recursively
                if os.path.isdir(file_path):
                    remove_folder(file_path)
                # If the file path is a file, delete it
                else:
                    os.remove(file_path)
            # After deleting all the files and folders in the directory, remove the directory itself
            os.rmdir(path)
            log_write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {BLUE}Removed folder: {END}{path}\n")
        else:
            # If the given path is not a directory, raise an error
            raise ValueError(f"{path} is not a directory")
    else:
        # If the given path does not exist, raise an error
        raise ValueError(f"{path} does not exist")


# **********************************************************************************
# Function schedule
# **********************************************************************************
def schedule(sch_interval):
    while True:

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

# src_path = sys.argv[1]
# dst_path = sys.argv[2]
# log_file_path = sys.argv[3]


sch_interval = 5  # in seconds
src_path = '/Users/alin/hyperiondev/sync/source'
dst_path = '/Users/alin/hyperiondev/sync/target'
log_file_path = '/Users/alin/hyperiondev/sync/log.txt'

schedule(sch_interval)
