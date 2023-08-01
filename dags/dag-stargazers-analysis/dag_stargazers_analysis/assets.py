from dagster import (
    AssetExecutionContext,
    MetadataValue,
    AssetIn,
    asset,
    Config,
    get_dagster_logger,
)

class MyAssetConfig(Config):
    git_repos: list


@asset(group_name="stargazers")
def get_gitrepos_list(context: AssetExecutionContext, config: MyAssetConfig) -> None:
    """
    Get list of git repositories provided run configuration.
    """

    context.add_output_metadata(
        metadata={
            "git_repos": str(config.git_repos), 
        }
    )
