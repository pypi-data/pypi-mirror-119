# Treewalker

A simple package to walk a directory tree and collect files and sizes into a SQLite DB.

## Usage

For simple use cases, simply install the package from PyPI:
```commandline
pip install treewalker
```
And run it from the command line:
```commandline
treewalker --help
treewalker --output test.sqlite --path C:/temp
```

## Usage and development

Get started (change directory to where you want the project first):
```commandline
pip install treewalker
```

Run the script with your own .json configuration:
```commandline
python treewalker.py --cfg my_config.json
```

```my_config.json
{
    "output": "test.sqlite",
    "path": "c:/temp"
}
```

Or run the script entirely from the command line:
```commandline
python walker.py --output test.sqlite --path c:\temp
```

Or build a single file executable if you need this to run on Windows systems that won't have Python pre-installed:
```commandline
scripts/build_pyinstaller.bat c:/target/folder
scripts/build_pyinstaller_xp.bat c:/target/folder

```
This creates a `treewalker.exe`, which can be run 'anywhere':
```commandline
.\treewalker.exe --output test.sqlite --path c:\temp
```

Note that the executable will be limited to running on systems that support the version of Python you're using to build it. I.e. for Windows XP (32-bit or 64-bit), the very latest version of Python you can use is 3.4.4.
