# Overleaf-Backup
Python library to backup self-hosted Overleaf projects

### Installation
The library can easily be installed with pip by running:

```shell
python -m pip install overleaf-backup
```

You can also download the files in the ```builds/``` directory and install it locally:

```shell
python -m pip install <filename>
```

### Usage
There are three different methods on how to backup your projects:

1. Backup only one time and use the overleaf credentials:

```python
from overleaf_backup.backup import *

execute_backup(projects=["012345678901234567890123"], 
               email="email@example.com", 
               password="examplePassword",
               url="https://overleaf.example.com", 
               backup_path="backups/")
```

2. Backup only one time and use the overleaf session cookie:

```python
from overleaf_backup.backup import *

execute_backup_cookie(
    projects = ["012345678901234567890123"],
    cookie="s%3An-C-Xs-rgxfxbR9AvTVxy_Yjrl2FcgXy.qRsTU\
            v4WxYZOTrxla8BiWQtl3Lkfrj%2BWYxqTkM%2B4lls",
    url="https://overleaf.example.com", 
    backup_path="backups/")
```

3. Backup the whole time with a given interval between two backups:  
   (You have to use the overleaf credentials here)

```python
from overleaf_backup.backup  import *

backup = BackupLoop(projects=["012345678901234567890123"], 
                    email="email@example.com", 
                    password="examplePassword",
                    url="https://overleaf.example.com", 
                    backup_path="backups/", 
                    interval=datetime.timedelta(days=1))
backup.execute()
```

The examples on how to use the library can also be found in the ```examples/``` 
directory.

### How are the backups stored?

The backups are stored in a zip file. Just unzip the file to get access to the
project files.