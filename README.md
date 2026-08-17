# SHA-256 File Integrity Checker

A lightweight Python 3 tool for monitoring file integrity using **SHA-256 cryptographic hashes**.

The program recursively scans the current directory and maintains a hash database in `hashLog.txt`. The stored hashes can then be used to detect files that have been:

* Modified
* Created
* Deleted

The script itself and `hashLog.txt` are automatically excluded from the analysis.

## Features

*  SHA-256 file hashing
*  Recursive directory scanning
*  Detect modified files
*  Detect new files
*  Detect deleted files
*  Automatically excludes the running script and `hashLog.txt`
*  No external dependencies
*  Python 3
*  Built-in command-line help

## Requirements

* Python 3.x

No external packages are required.

## Usage

### Generate the hash database

Run:

```bash
python3 hash.py hash
```

This recursively scans the current directory, calculates the SHA-256 hash of every file, and creates:

```text
hashLog.txt
```

The log contains entries in the following format:

```text
SHA256  path/to/file
```

Example:

```text
a8c3f9...  index.php
91b2e7...  includes/sql.php
4f8a12...  css/style.css
```

### Verify file integrity

Run:

```bash
python3 hash.py verify
```

The program compares the current filesystem state against `hashLog.txt`.

If no changes are detected:

```text
[OK] No changes detected.
```

If changes are found:

```text
[!] 3 change(s) detected:

MODIFIED:
  index.php
  includes/sql.php

NEW:
  uploads/new.php

DELETED:
  old/test.php
```

The `verify` command does **not** modify the hash database.

## Help

Display the available commands and options:

```bash
python3 hash.py --help
```

## Recommended Workflow

First, create a baseline of the current filesystem:

```bash
python3 hash.py hash
```

Then periodically verify its integrity:

```bash
python3 hash.py verify
```

If nothing has changed:

```text
[OK] No changes detected.
```

Otherwise, the program reports all modified, newly created, or deleted files.

## Excluded Files

The following files are automatically excluded from the scan:

```text
hashLog.txt
```

as well as the script currently being executed.

This prevents the hash database from being detected as a modified file and avoids the script attempting to hash itself.

## Security Considerations

SHA-256 provides a reliable way to detect changes to file contents.

However, `hashLog.txt` should be considered part of the **trusted baseline**. An attacker with sufficient permissions to modify the monitored files could potentially modify the hash database as well.

For stronger protection, keep a copy of `hashLog.txt` in a protected or separate location.

## License

Specify the license for this project here.
