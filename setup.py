import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="entity_resolution_evaluation",
    version="0.0.1",
    author="Paul Boosz",
    author_email="paulboosz@gmail.com",
    description="An implementation of the generalized merged distance to evaluate entity resolution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paulboosz/entity-resolution-evaluation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)