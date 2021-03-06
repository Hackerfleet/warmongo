# hfoswarmongo
# ============
# Copyright 2013 Rob Britton
# Copyright 2015 riot <riot@hackerfleet.org> and others.
#
# This file has been changed and this notice has been added in
# accordance to the Apache License
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .model import Model as WarmongoModel
from .exceptions import InvalidSchemaException

from copy import deepcopy
from .database import connect
import pymongo

# Export connect so we can do warmongo.connect()
connect = connect

# Export some constants from pymongo
ASCENDING = pymongo.ASCENDING
DESCENDING = pymongo.DESCENDING


def model_factory(schema, base_class=WarmongoModel):
    ''' Construct a model based on `schema` that inherits from `base_class`. '''
    if not schema.get("id"):
        raise InvalidSchemaException("No id field in schema!")

    if not schema.get("properties"):
        raise InvalidSchemaException("No properties field in schema!")

    if not schema.get("name"):
        raise InvalidSchemaException("Warmongo models require a top-level 'name' attribute!")

    schema = deepcopy(schema)

    class Model(base_class):
        _schema = schema

        def __init__(self, *args, **kwargs):
            self._schema = schema
            base_class.__init__(self, *args, **kwargs)

    Model.__name__ = str(schema["name"])

    return Model
