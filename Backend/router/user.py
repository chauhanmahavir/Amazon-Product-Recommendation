from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from config.settings import constants
from schemas.user import UserResponse
from services.db import connect_snowflake, get_random_user_ids, get_purchased
from services.sagemaker_api import get_prediction

router = APIRouter()

session = connect_snowflake()

@router.get("/get_user_id")
async def login() -> JSONResponse:
    try:
        random_user_ids = get_random_user_ids(session, 10)
        response = UserResponse()
        response.message = constants.SUCCESS
        response.random_user_ids = random_user_ids
        return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = UserResponse()
        response.message = str(e)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/predict")
async def singup(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        user_id = body["user_id"]
        response = UserResponse()
        response.message = constants.SUCCESS
        response.user_id = user_id
        response.prediction = get_prediction(user_id)
        response.purchased = get_purchased(session, user_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = UserResponse()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))