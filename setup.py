import setuptools

with open("requirements.txt") as f:
    install_reqs = f.read().splitlines()

with open("dev-requirements.txt") as f:
    dev_install_reqs = f.read().splitlines()

setuptools.setup(
    name="stocklake",
    version="0.0.4",
    py_modules=["stocklake"],
    install_requires=install_reqs,
    packages=setuptools.find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    extras_require={"dev": dev_install_reqs},
    entry_points={
        "console_scripts": [
            "stocklake = stocklake.cli:cli",
        ],
    },
)
