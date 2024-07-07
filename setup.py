from setuptools import find_packages, setup

setup(
    name="torch-submit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "rich",
        "pyyaml",
        "fabric",
    ],
    entry_points={
        "console_scripts": [
            "torch-submit=torch_submit.cli:app",
        ],
    },
)