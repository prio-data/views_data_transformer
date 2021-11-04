import environs

env = environs.Env()
env.read_env()

LOG_LEVEL = env.str("LOG_LEVEL","WARNING").upper()

ROUTER_URL = env.str("ROUTER_URL","http://router")
