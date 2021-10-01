import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anki-cli-unofficial",
    version="1.0.3",
    author="Julien Sobczak",
    description="A CLI to load flashcards in Anki2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/julien-sobczak/anki-cli",
    scripts=['./scripts/anki-cli-unofficial'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'setuptools',
        'pyyaml'
    ],
    python_requires='>=3.6',
)
