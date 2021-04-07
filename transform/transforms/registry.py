
from . import util,exceptions

_TRANSFORMS = {
    "priogrid_month":{
        "identity": util.identity 
    },
    "country_month":{
        "identity": util.identity 
    }
}

def get_transform(loa,name):
    try:
        return _TRANSFORMS[loa][name]
    except KeyError as ke:
        raise exceptions.NotRegistered from ke
