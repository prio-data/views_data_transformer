
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

env = environs.Env()
env.read_env()
config = env
