import json
import logging
from fastapi import Request

from fastapi import APIRouter, HTTPException, Depends
from fast_api_als.database.db_helper import db_helper_session
from fast_api_als.services.authenticate import get_token
from fast_api_als.utils.cognito_client import get_user_role
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

router = APIRouter()

logging.basicConfig(filename='three_pl.log', format="%(levelname)s: %(message)s", level=logging.DEBUG)

@router.post("/reset_authkey")
async def reset_authkey(request: Request, token: str = Depends(get_token)):
    body = await request.body()
    try:
        body = json.loads(body)
    except ValueError:
        logging.error("JSON format invalid")
        raise ValueError
    provider, role = get_user_role(token)
    if role != "ADMIN" and (role != "3PL"):
        logging.info(f'The role is not ADMIN or 3PL')
        pass
    if role == "ADMIN":
        provider = body['3pl']
    logging.info(f'Trying to update API key')
    try:
        apikey = db_helper_session.set_auth_key(username=provider)
    except Exception as e:
        logging.error(f'The API key could not be updated')
        raise e
    logging.info(f'API key successfully updated')
    return {
        "status_code": HTTP_200_OK,
        "x-api-key": apikey
    }


@router.post("/view_authkey")
async def view_authkey(request: Request, token: str = Depends(get_token)):
    body = await request.body()
    try:
        body = json.loads(body)
    except ValueError:
        logging.error(f'Body not in JSON format')
        raise ValueError
    provider, role = get_user_role(token)

    if role != "ADMIN" and role != "3PL":
        pass
    if role == "ADMIN":
        provider = body['3pl']
    logging.info(f'Trying to update API key')
    try:
        apikey = db_helper_session.set_auth_key(username=provider)
    except Exception as e:
        logging.error(f'The API key could not be updated')
        raise e
    logging.info(f'API key successfully updated')
    return {
        "status_code": HTTP_200_OK,
        "x-api-key": apikey
    }
