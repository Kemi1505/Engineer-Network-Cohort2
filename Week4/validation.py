# validate all incoming requests
from marshmallow import Schema, fields, validate, ValidationError

class UserRegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))

class PostSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=3, max=400))
    content = fields.Str(required=True, validate=validate.Length(min=3))