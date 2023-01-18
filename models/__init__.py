# Here we write Models for MongoDB
from models.schemas.userschema import UserSchema, UserSchemaWithoutPWD
from models.schemas.objectschema import ObjectSchema
from models.schemas.placeschema import PlaceSchema
models = [UserSchema, ObjectSchema, PlaceSchema]
