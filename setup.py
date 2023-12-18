import setuptools

setuptools.setup(
    name="stocklake",
    version="0.0.3",
    py_modules=["stocklake"],
    install_requires=[
        "Click",
    ],
    packages=setuptools.find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "stocklake = stocklake.cli:cli",
        ],
    },
)
