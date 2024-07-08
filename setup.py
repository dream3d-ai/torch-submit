from setuptools import find_packages, setup

setup(
    name="torch-submit",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
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