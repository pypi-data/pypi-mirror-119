# AutoBackuper

Python3 utility for backing up files. Intended use is to automatically back up word or latex files in case of corruption or need to reference an older version of a file.

# Usage

Navigate to the folder where you want git repository to be located and execute: 

`autobackuper FILENAME [poll interval in seconds]`

Utility will init a git repository, after that specifie file will be checked for changes, and automatically commited.

# Requirements

- git must be available in path