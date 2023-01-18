import bson
import mongoengine.errors
from bson.errors import InvalidId
from fastapi_jwt import JwtAuthorizationCredentials

from fastapi import APIRouter, Path, HTTPException, Form, Security
from fastapi.responses import JSONResponse
from models import UserSchema, UserSchemaWithoutPWD, ObjectSchema
from loguru import logger

from models.mongo_models import Items
from models.schemas.objectschema import ObjectSchemaPatch
from models.schemas.userschema import AccessToken
from .authorization import access_security
from .crud import retrieving_user_with_cred, create_user as create_user_crud

router = APIRouter(prefix='/api/users')


@router.post('', response_model=UserSchema)
async def create_user(user: UserSchema):
    user = await create_user_crud(user)
    return user.to_dict()


@router.get('/user/{user_id}', response_model=UserSchemaWithoutPWD)
async def retrieve_user(user_id: str = Path(title='User unique identifier')):
    try:
        user = await retrieving_user_with_cred(id=user_id)
    except mongoengine.errors.ValidationError as exc:
        return JSONResponse(status_code=400, content={"detail": str(exc)})
    return user.to_dict()


@router.post('/auth', response_model=AccessToken)
async def auth(username: str = Form(), password: str = Form()):
    user = await retrieving_user_with_cred(username=username, password=password)
    subject = {
        'user_id': str(user.id)
    }
    return {
        'user_id': str(user.id),
        'access_token': access_security.create_access_token(subject=subject)
    }


@router.post('/token/validate', response_model=AccessToken)
async def validate_token(credentials: JwtAuthorizationCredentials = Security(access_security)):
    user = await retrieving_user_with_cred(id=credentials.subject['user_id'])
    subject = {
        'user_id': str(user.id)
    }
    return {
        'user_id': str(user.id),
        'access_token': access_security.create_access_token(subject=subject)
    }


@router.get('/list-items')
async def list_user_items(credentials: JwtAuthorizationCredentials = Security(access_security)):
    user = await retrieving_user_with_cred(id=credentials.subject['user_id'])
    return [x.to_dict() for x in Items.objects(id__in=user.items)]


@router.get('/list-all-items')
async def list_all_items(credentials: JwtAuthorizationCredentials = Security(access_security)):
    user = await retrieving_user_with_cred(id=credentials.subject['user_id'])
    if not user.is_admin:
        raise HTTPException(status_code=405, detail="You are not admin user")
    return [x.to_dict() for x in Items.objects()]


@router.post('/create-item')
async def create_item(item: ObjectSchema, credentials: JwtAuthorizationCredentials = Security(access_security)):
    user = await retrieving_user_with_cred(id=credentials.subject['user_id'])
    if not user.is_admin:
        raise HTTPException(status_code=405, detail="You are not admin user")
    item = Items(**item.dict())
    item.save()
    return item.to_dict()


@router.patch('/patch-item/{item_id}')
async def patch_item(item: ObjectSchemaPatch, item_id: str = Path(title="item unique identifier"),
                     credentials: JwtAuthorizationCredentials = Security(access_security)):
    user = await retrieving_user_with_cred(id=credentials.subject['user_id'])
    if not user.is_admin:
        raise HTTPException(status_code=405, detail="You are not admin user")
    item_obj: Items = Items.objects.get(id=item_id)

    for key, val in item.dict().items():
        if key == 'master':
            try:
                bson.ObjectId(val)
                user = await retrieving_user_with_cred(id=val)
            except InvalidId:
                user = await retrieving_user_with_cred(username=val)
            val = user.id

        if val is not None:
            setattr(item_obj, key, val)
            continue
    item_obj.save()

    return item_obj.to_dict()
