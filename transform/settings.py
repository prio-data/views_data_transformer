
"""
Required settings:
* Env:
    - KEY_VAULT_URL
* Config:
    - ROUTER_URL
    - TIME_CASTER_URL
    - LOG_LEVEL
"""
import environs
from fitin import views_config

env = environs.Env()
env.read_env()
config = views_config(env.str("KEY_VAULT_URL"))
