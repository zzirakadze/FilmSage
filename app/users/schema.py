from marshmallow import Schema, fields, validate


class GetUsersSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email())
