import setuptools

# with open("requirements.txt") as f:
#     install_reqs = f.read().splitlines()

# with open("dev-requirements.txt") as f:
#     dev_install_reqs = f.read().splitlines()

with open("README.md") as f:
    load_description = f.read()

setuptools.setup(
    name="stocklake",
    version="0.0.7",
    py_modules=["stocklake"],
    install_requires=[
        "polygon-api-client",
        "python-dotenv",
        "pandas",
        "click",
        "requests",
    ],
    packages=setuptools.find_packages(),
    long_description=load_description,
    long_description_content_type="text/markdown",
    extras_require={"dev": ["ruff-lsp", "black"]},
    entry_points={
        "console_scripts": [
            "stocklake = stocklake.cli:cli",
        ],
    },
)
