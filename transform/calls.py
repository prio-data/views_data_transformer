
import os
from datetime import date
import requests
from settings import config

def vmid(tgt_date):
    response = requests.get(
            os.path.join(config("TIME_CASTER_URL"),
                "vmid",str(tgt_date))
            )
    return int(response.content.decode())

def get_year_month_id_bounds(year:int):
    start = vmid(date(year=year,month=1,day=1))
    end = vmid(date(year=year,month=12,day=1))
    return start,end
