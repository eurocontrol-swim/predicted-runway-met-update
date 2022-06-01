import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="predicted-runway-met-update",
    version="0.0.1",
    author="EUROCONTROL (SWIM)",
    author_email="francisco-javier.crabiffosse.ext@eurocontrol.int",
    description="Keeps up to date a DB with AVWX (METAR, TAF) data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eurocontrol-swim/predicted-runway-met-update",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'pymongo',
        'mongoengine',
        'opnieuw',
        'APScheduler',
        'git+https://git@github.com/eurocontrol-swim/predicted-runway-met-update-db.git'
    ],
    license='see LICENSE'
)
