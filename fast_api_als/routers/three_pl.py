import json
import logging
from fastapi import Request

from fastapi import APIRouter, HTTPException, Depends
from fast_api_als.database.db_helper import db_helper_session
from fast_api_als.services.authenticate import get_token
from fast_api_als.utils.cognito_client import get_user_role
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from ..main import custom_logger

router = APIRouter()
logger = custom_logger.getLogger(__main__)

@router.post("/reset_authkey")
async def reset_authkey(request: Request, token: str = Depends(get_token)):
    body = await request.body()
    try:
        body = json.loads(body)
    except ValueError:
        logger.error("JSON format invalid")
        raise ValueError
    provider, role = get_user_role(token)
    if role != "ADMIN" and (role != "3PL"):
        logger.info(f'The role is not ADMIN or 3PL')
        pass
    if role == "ADMIN":
        provider = body['3pl']
    logger.info(f'Trying to update API key')
    try:
        apikey = db_helper_session.set_auth_key(username=provider)
    except Exception as e:
        logger.error(f'The API key could not be updated')
        raise e
    logger.info(f'API key successfully updated')
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
        logger.error(f'Body not in JSON format')
        raise ValueError
    provider, role = get_user_role(token)

    if role != "ADMIN" and role != "3PL":
        pass
    if role == "ADMIN":
        provider = body['3pl']
    logger.info(f'Trying to update API key')
    try:
        apikey = db_helper_session.set_auth_key(username=provider)
    except Exception as e:
        logger.error(f'The API key could not be updated')
        raise e
    logger.info(f'API key successfully updated')
    return {
        "status_code": HTTP_200_OK,
        "x-api-key": apikey
    }
