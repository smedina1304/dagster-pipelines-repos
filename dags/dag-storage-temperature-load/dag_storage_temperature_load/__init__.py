import os

from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
    mem_io_manager,
    in_process_executor,
    RunConfig
)

from cryptography.fernet import Fernet
from office365.sharepoint.client_context import ClientContext, UserCredential
# INSTALL: pip install Office365-REST-Python-Client

from . import assets

all_assets = load_assets_from_modules([assets])

# Define a job that will materialize the assets
storage_temperature_job = define_asset_job(name="storage_temperature_job", selection=AssetSelection.all())

# Schedule Definition
storage_temperature_schedule = ScheduleDefinition(
    job=storage_temperature_job,
    cron_schedule="*/30 * * * *",  # At every 30th minute. https://crontab.guru/every-15-minutes
)

# Password - Cryptography/Fernet
fernet_key : str = os.environ["MY_FERNET_KEY"]
fernet_key = fernet_key.encode()
f = Fernet(fernet_key)

encrypted_pwd : str = os.environ["STORAGE_TEMPERATURE_PASSWORD"]
encrypted_pwd = encrypted_pwd.encode()
decrypted_pwd = f.decrypt(encrypted_pwd)

# Sharepoint UserCredential/ClientContext
url_site = 'https://afonline.sharepoint.com/sites/PowerAppsDEV'
user_credentials = UserCredential(os.environ["STORAGE_TEMPERATURE_USER"],decrypted_pwd.decode())

# Assets Definitions
defs = Definitions(
    assets=all_assets,
    schedules=[storage_temperature_schedule],
    resources={
        "url_site": url_site,
        "user_credentials": user_credentials,
        "data_path": 'data/dags/storagetemp',
        "file_name": 'df_storagetemp.csv',
        "supabase_url": os.environ["SUPABASE_URL"],
        "supabase_key": os.environ["SUPABASE_KEY"],
        "supabase_token": os.environ["SUPABASE_TOKEN"]
    }  
)
