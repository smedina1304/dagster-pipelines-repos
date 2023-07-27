from setuptools import find_packages, setup


setup(
    name="dag_hackernews_report",
    packages=find_packages(exclude=["dag_hackernews_report_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
