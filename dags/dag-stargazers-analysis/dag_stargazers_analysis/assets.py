import os
import pandas as pd

from datetime import datetime, timedelta
from dagster import (
    AssetExecutionContext,
    MetadataValue,
    AssetIn,
    asset,
    Config,
    get_dagster_logger
)

class MyAssetConfig(Config):
    github_repos: list
    data_path = 'data/dags/hackernews'
    dataset_name = 'df_github_stargazers.csv'  

@asset(group_name="stargazers")
def get_github_repos(context: AssetExecutionContext, config: MyAssetConfig) -> list:
    """
    Get list of git repositories provided run configuration.
    """

    repos = config.github_repos

    context.add_output_metadata(
        metadata={
            "github_repos": str(repos),
            "data_path" : 'data/dags/stargazers',
            "dataset_name" : 'df_github_stargazers.csv'  
        }
    )

    return repos


@asset(
        group_name="stargazers", 
        required_resource_keys={"github_api"},
        ins={"repos": AssetIn("get_github_repos")}
    )
def get_github_stargazers(context: AssetExecutionContext, config: MyAssetConfig) -> None:
    """
    Get of stargazers data from each repository informed in the List.
    """
    logger = get_dagster_logger()
    path_file = f'{config.data_path}/{config.dataset_name}'
    df = None

    try:
        dtfile = datetime.fromtimestamp(os.path.getmtime(path_file))
        if datetime.now().date() == dtfile.date():
            df = pd.read_csv(path_file)
            logger.info(f"Dataframe was loaded from: {path_file}")
    except OSError as e:
        logger.info(f"File not found: {path_file}")
        logger.info(f"Exception: {e.strerror}")
        df = None

    if df == None:
        for repo in config.github_repos:
            print(repo)
            logger.info(f"Get Repo stargazers with dates: {path_file}")
            repo_stargazers = list(
                context.resources.github_api.get_repo(repo).get_stargazers_with_dates()
            )

            dfrepo = pd.DataFrame(
                [
                    {
                        "users": stargazer.user.login,
                        "date": stargazer.starred_at.date(),
                        "week": stargazer.starred_at.date()
                        + timedelta(days=6 - stargazer.starred_at.weekday()),
                    }
                    for stargazer in repo_stargazers
                ]
            )

            dfrepo['repo'] = repo

            if df is None:
                df = dfrepo.copy()
            else:
                df = pd.concat([df, dfrepo], ignore_index=True)

            del dfrepo

    df.to_csv(path_file)
