from setuptools import setup, find_packages

setup(
    name="kirilov_updater",  # Package name (unique in PyPI)
    version="1.0.0",  # Initial version
    description="A python package to automatically check updates on open source projects.",
    author="Kirilov",
    author_email="kirilovcode@gmail.com",
    url="https://github.com/yourusername/check-for-updates",  # Update with your GitHub URL
    packages=find_packages(),
    install_requires=[
        "requests>=2.0.0",
        "beautifulsoup4>=4.0.0",
        "packaging>=20.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
