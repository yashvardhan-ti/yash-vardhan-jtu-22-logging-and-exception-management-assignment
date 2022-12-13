import calendar
import time
import logging
import math
from dateutil import parser
from fast_api_als.database.db_helper import db_helper_session

from fast_api_als import constants

"""
what exceptions can be thrown here?
"""


def get_enriched_lead_json(adf_json: dict) -> dict:
    if adf_json is not dict:
        raise ValueError(f'given paramerter {adf_json} is invalid')
        return