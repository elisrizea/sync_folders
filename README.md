
# **Sync Folders using only Python 3's built-in modules**
    Sync two folders periodically using only Python 3's built-in modules. Command-line arguments provide folder paths, sync interval, and log file path.
    Compare folder contents using a recursive function, updating destination folder accordingly. Undo changes made directly to the destination folder.
    Record changes in log file.


# **Description:**
    The MIRROR folder is periodically synced with the SOURCE folder to update any changes made to the SOURCE folder. Recursive function calls 
    are use to navigates the directory tree of both folders to identify any differences between the two. For files that exist in both folders,
    their timestamps and sizes are compared, and the MIRROR file is updated if necessary. The process is repeated at the chosen interval to keep
    the MIRROR folder up-to-date with the SOURCE folder. Any changes made directly to the MIRROR folder that are not found in the SOURCE 
    folder are undone during the synchronization process. 
    Version 2 will add SSH support for network synchronization between remote machines, using only Python 3's built-in modules.


# **Require:**
    Python 3 Interpreter

# **Running:**
    sync.py <source_folder> <target_folder> <log_folder> <sync_interval(hh:mm:ss)>

# **Credits:**
    Alin Rizea
    https://www.linkedin.com/in/alin-rizea-b10368104/


