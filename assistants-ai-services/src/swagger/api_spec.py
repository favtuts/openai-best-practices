"""OpenAPI v3 Specification"""

# apispec via OpenAPI
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
import src.utils.log_manager as log_manager

logger = log_manager.get_logger(__name__)

# create an APISpec
spec = APISpec(
    title="emTeller AI Services",
    version="2.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# define Schemas
class InputSchema(Schema):
    number = fields.Int(description="An integer", required=True)

class OutputSchema(Schema):
    msg = fields.String(description="A message", required=True)


# register schema with spec
spec.components.schema("Input", schema=InputSchema)
spec.components.schema("Output", schema=OutputSchema)

# add swagger tags that are used for endpoint annotation
tags = [
            {'name': 'testing',
             'description': 'For testing the API.'
            },
            {'name': 'calculation',
             'description': 'Functions for calculating.'
            },
       ]

for tag in tags:
    logger.debug(f"Adding tag: {tag['name']}")
    spec.tag(tag)