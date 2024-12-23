import requests
from bs4 import BeautifulSoup
from packaging.version import Version
import zipfile
import os

class UpdateChecker:
    def __init__(self, project, repo, branch):
        self.project = project
        self.repo = repo
        self.branch = branch
        self.version_url = f"https://raw.githubusercontent.com/{project}/{branch}/VERSION"
        self.archive_url = f"https://github.com/{project}/archive/refs/heads/{branch}.zip"

    def get_current_version(self):
        try:
            response = requests.get(self.version_url)
            response.raise_for_status()
            html = response.text
            soup = BeautifulSoup(html, features="html.parser")
            return Version(soup.text.strip())
        except Exception as e:
            print(f"Error fetching version: {e}")
            return None

    def download_and_extract(self):
        download_path = "temp.zip"
        extract_path = "."
        target_folder = f"{self.repo}-{self.branch}/"

        try:
            response = requests.get(self.archive_url, stream=True)
            response.raise_for_status()
            with open(download_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=10 * 1024):
                    file.write(chunk)

            with zipfile.ZipFile(download_path, "r") as zip_ref:
                os.makedirs(extract_path, exist_ok=True)
                for file_name in zip_ref.namelist():
                    if file_name.startswith(target_folder):
                        relative_path = os.path.relpath(file_name, target_folder)
                        if relative_path == ".":
                            continue
                        target_path = os.path.join(extract_path, relative_path)
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        if not file_name.endswith("/"):
                            with open(target_path, "wb") as target_file:
                                target_file.write(zip_ref.read(file_name))
                            print(f"Extracted: {file_name} to {target_path}")
            os.remove(download_path)
        except Exception as e:
            print(f"Error downloading or extracting files: {e}")

    def check_for_updates(self):
        current_version = self.get_current_version()
        if not current_version:
            print("Failed to fetch the current version.")
            return

        base_version = Version(open("VERSION", "r").read())

        if current_version > base_version:
            print("New update available. Downloading and extracting...")
            self.download_and_extract()
        elif current_version < base_version:
            print("Files are corrupted! Restoring...")
        else:
            print("No new updates detected.")

# Example usage
'''
if __name__ == "__main__":
    checker = UpdateChecker("feketefh/pady", "pady", "main")
    checker.check_for_updates()
'''