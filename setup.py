from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="date_clean",
    version="0.1.4",
    author="Gerick Toro",
    author_email="gerickt@gmail.com",
    description="Librería para homogenización de fechas en español.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/gerickt/date_clean',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'python-dateutil',
        'pytz',
        'tzdata',  # Agrega tzdata a la lista de dependencias

    ],
    python_requires=">=3.9",
)
