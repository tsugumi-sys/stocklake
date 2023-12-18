from setuptools import setup

setup(
    name="stocklake",
    version="0.1.0",
    py_modules=["stocklake"],
    install_requires=[
        "Click",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "stocklake = stocklake.cli:cli",
        ],
    },
)
