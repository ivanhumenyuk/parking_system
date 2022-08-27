"""General schemas"""

from flask_marshmallow import Schema
from marshmallow import fields as f


class SimpleMessageSchema(Schema):
    message = f.String()
