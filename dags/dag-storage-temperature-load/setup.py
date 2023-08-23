from setuptools import find_packages, setup

setup(
    name="dag_storage_temperature_load",
    packages=find_packages(exclude=["dag_storage_temperature_load_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
