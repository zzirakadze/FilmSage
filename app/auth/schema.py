from marshmallow import Schema, fields, validate

from .models import Auth


class UserRegistrationSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    surname = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True, validate=Auth.validate_email_format)
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=Auth.validate_password_format)


class UserLoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=Auth.validate_password_format)
