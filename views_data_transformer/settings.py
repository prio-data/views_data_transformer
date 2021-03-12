
from environs import Env
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.appconfiguration import AzureAppConfigurationClient

env = Env()
env.read_env()

KEY_VAULT_URL = env.str("KEY_VAULT_URL") 

app_config_client = AzureAppConfigurationClient.from_connection_string(
        (SecretClient(KEY_VAULT_URL,DefaultAzureCredential())
            .get_secret("app-settings-connection-string")
            .value
        )
)

ROUTER_URL = app_config_client.get_configuration_setting("data-router-url").value

TIME_CASTER_URL = app_config_client.get_configuration_setting("time-caster-url").value

