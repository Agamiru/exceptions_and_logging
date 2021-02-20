import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="exceptions_and_logging",
    version="0.0.2",
    author="Chidi Nnadi",
    author_email="chidinnaemekannadi@gmail.com",
    description="A Django app for logging custom application errors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Agamiru/exceptions_and_logging",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django :: 3.0"
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
