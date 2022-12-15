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
    try:
        key = input('search for key: ')
        print(f'The value for {key} key is {adf_json[key]}')
    except KeyError:
        print(f'The value for {key} does not exist'.format(key))