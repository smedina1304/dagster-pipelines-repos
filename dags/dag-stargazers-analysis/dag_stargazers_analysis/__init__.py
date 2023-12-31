import os
from github import Github

from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
    RunConfig
)

from . import assets

all_assets = load_assets_from_modules([assets])

# Define a job that will materialize the assets
stargazers_job = define_asset_job(
    name="stargazers_job", 
    #selection=AssetSelection.all(),
    config=RunConfig(
        {"get_github_stargazers": 
         assets.MyAssetConfig(
            github_repos=[
                    "dagster-io/dagster",
                    "apache/airflow",
                    "PrefectHQ/prefect",
                    "mage-ai/mage-ai",
                    "kestra-io/kestra"
                ]
            )
        }
    )
)

# Addition: a ScheduleDefinition the job it should run and a cron schedule of how frequently to run it
stargazers_schedule = ScheduleDefinition(
    job=stargazers_job,
    cron_schedule="0 8 * * 1",  # at 08:00 on Monday.
)

defs = Definitions(
    assets=all_assets,
    schedules=[stargazers_schedule],
    resources={"github_api": Github(os.environ["GITHUB_ACCESS_TOKEN"])}
)
