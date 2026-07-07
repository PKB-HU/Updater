# UpdateChecker

`UpdateChecker` is a lightweight Python utility for checking whether a newer version of a GitHub-hosted project is available, and if so, downloading and extracting the latest files automatically.

It compares a local `VERSION` file with a remote `VERSION` file stored in a GitHub repository branch. If a newer version exists, it downloads the branch archive as a ZIP file and extracts its contents into the current directory.

---

## Features

* Fetches the latest version number from a GitHub repository
* Compares the remote version with a local `VERSION` file
* Downloads the latest branch archive when an update is available
* Extracts the archive contents directly into the current project directory
* Uses semantic version parsing via `packaging.version.Version`

---

## Requirements

Install the required dependencies before running the script:

```bash
pip install requests beautifulsoup4 packaging
```

---

## Project Structure

Your local project should contain a `VERSION` file with the currently installed version:

```text
project/
├── VERSION
├── updater.py
└── ...
```

The remote GitHub repository should also contain a `VERSION` file in the root of the target branch.

---

## How It Works

### 1. Check remote version

The script fetches the remote `VERSION` file from GitHub using:

```python
https://raw.githubusercontent.com/{project}/{branch}/VERSION
```

### 2. Compare versions

It compares the remote version with the local version stored in the local `VERSION` file.

### 3. Download update if needed

If the remote version is newer, it downloads the ZIP archive of the branch:

```python
https://github.com/{project}/archive/refs/heads/{branch}.zip
```

### 4. Extract project files

The ZIP archive is extracted into the current directory, preserving the project file structure while removing the top-level GitHub archive folder.

---

## Usage

### Example

```python
from updater import UpdateChecker

if __name__ == "__main__":
    checker = UpdateChecker("feketefh/pady", "pady", "main")
    checker.check_for_updates()
```

---

## Constructor Parameters

### `UpdateChecker(project, repo, branch)`

| Parameter | Type  | Description                                               |
| --------- | ----- | --------------------------------------------------------- |
| `project` | `str` | GitHub repository in the format `"owner/repository"`      |
| `repo`    | `str` | Repository name used to identify the extracted ZIP folder |
| `branch`  | `str` | Branch to check and download updates from                 |

### Example

```python
checker = UpdateChecker(
    project="feketefh/pady",
    repo="pady",
    branch="main"
)
```

---

## Methods

## `get_current_version()`

Fetches the remote `VERSION` file from GitHub and returns it as a parsed `Version` object.

### Returns

* `Version` object if successful
* `None` if fetching or parsing fails

---

## `download_and_extract()`

Downloads the repository branch as a ZIP archive and extracts its contents into the current working directory.

### Behavior

* Saves the ZIP temporarily as `temp.zip`
* Extracts files from the GitHub archive folder
* Removes the top-level archive directory name (for example, `pady-main/`)
* Deletes the temporary ZIP after extraction

---

## `check_for_updates()`

Main update workflow:

1. Fetches the remote version
2. Reads the local `VERSION` file
3. Compares both versions
4. Downloads and extracts files if an update is available

### Output cases

* **Remote version > local version**

  * Prints: `New update available. Downloading and extracting...`
  * Downloads and extracts the updated files

* **Remote version < local version**

  * Prints: `Files are corrupted! Restoring...`

* **Versions are equal**

  * Prints: `No new updates detected.`

---

## Example Output

### When an update is available

```text
New update available. Downloading and extracting...
Extracted: pady-main/file1.py to file1.py
Extracted: pady-main/module/utils.py to module/utils.py
```

### When already up to date

```text
No new updates detected.
```

### When the remote version cannot be fetched

```text
Error fetching version: ...
Failed to fetch the current version.
```

---

## Notes

* The local project must contain a valid `VERSION` file.
* The remote repository must also contain a `VERSION` file in the target branch root.
* Version strings should follow a format compatible with `packaging.version.Version`, such as:

```text
1.0.0
1.2.3
2.0.0rc1
```

* The updater currently extracts files directly into the current working directory, which may overwrite existing files.

---

## Limitations

* There is no rollback or backup mechanism before overwriting files.
* The `"Files are corrupted! Restoring..."` case currently only prints a message and does not restore files automatically.
* The script assumes the GitHub ZIP archive folder name follows the format:

```text
{repo}-{branch}/
```

This works for standard GitHub branch archive downloads.

---

## Recommended Improvements

If you plan to expand this updater, consider adding:

* Automatic backup before overwriting files
* File integrity checks (hash verification)
* Progress indicators for downloads
* Retry logic for network failures
* Automatic restore logic when local files are newer or corrupted
* Logging instead of `print()` statements
* Safer extraction with path validation

---

## License

Add your preferred license here, for example:

```text
MIT License
```
