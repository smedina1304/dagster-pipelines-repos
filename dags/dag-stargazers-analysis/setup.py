from setuptools import find_packages, setup

setup(
    name="dag_stargazers_analysis",
    packages=find_packages(exclude=["dag_stargazers_analysis_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
